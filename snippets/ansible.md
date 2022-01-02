# Ansible

```yaml
nfs_mounts:
  - name: Media
    server_path: 192.168.1.30:/mnt/nfs-data/media
    mount_point: /nfs/Media
    systemd_filename: nfs-Media.mount
  - name: Nextcloud
    server_path: 192.168.1.30:/mnt/nfs-data/nextcloud
    mount_point: /nfs/Nextcloud
    systemd_filename: nfs-Nextcloud.mount
```

```yaml
- name: Create NFS mount points
  ansible.builtin.file:
  path: "{{ item.mount_point }}"
  state: directory
  mode: 0755
  loop: "{{ nfs_mounts }}"

- name: Install systemd mounts
  ansible.builtin.blockinfile:
  path: "/etc/systemd/system/{{ item.systemd_filename }}"
  create: true
  mode: 0644
  block: |
    [Unit]
    Description={{ item.name }}

    [Mount]
    What={{ item.server_path }}
    Where={{ item.mount_point }}
    Options=auto
    Type=nfs

    [Install]
    WantedBy=multi-user.target
  loop: "{{ nfs_mounts }}"

- name: Reload systemd daemon
  ansible.builtin.systemd:
  daemon_reload: true

- name: Mount NFS shares
  ansible.builtin.systemd:
  name: "{{ item.systemd_filename }}"
  state: started
  enabled: true
  loop: "{{ nfs_mounts }}"
```

 ---

 ```yaml
 - name: Purge Snaps and snapd
  block:
    - name: Get list of installed Snaps
      ansible.builtin.find:
        paths: /var/snap
        recurse: false
        file_type: directory
        patterns: "^(?!snapd).*$"
        use_regex: true
      register: installed_snaps
    - name: Uninstall non-core Snaps
      vars:
        snap: "{{ item['path'] | basename }}"
      community.general.snap:
        name: "{{ snap }}"
        state: absent
      loop: "{{ installed_snaps['files'] }}"
      when: "'core' not in snap"
    - name: Uninstall core Snaps
      vars:
        snap: "{{ item['path'] | basename }}"
      community.general.snap:
        name: "{{ snap }}"
        state: absent
      loop: "{{ installed_snaps['files'] }}"
      when: "'core' in snap"
    - name: Uninstall snapd
      community.general.snap:
        name: snapd
        state: absent
    - name: Unmount snap directories
      ansible.posix.mount:
        path: "{{ item['mount'] }}"
        state: unmountqed
      loop: "{{ ansible_mounts }}"
      when: "('/snap/core' in item['mount']) or ('/var/snap' in item['mount'])"
    - name: Remove snap directories
      ansible.builtin.file:
        path: "{{ item }}"
        state: absent
      loop: ["/snap", "/var/snap", "/var/lib/snapd", "{{ ansible_user_dir }}/snap"]
    - name: Hold the snapd package
      dpkg_selections:
        name: snapd
        selection: hold
  become: true
  when: "'desktop' in system_type"
```

---

```yaml
- name: Configure Docker prereqs and pull containers
  block:
    - name: Add user to 'docker' group
      ansible.builtin.user:
        name: "{{ ansible_user_id }}"
        groups: docker
        append: true
    - name: Ensure Docker is running
      ansible.builtin.systemd:
        name: docker
        daemon_reload: true
        enabled: true
        state: started
    - name: Pull latest container images via Docker
      environment:
        PYTHONPATH: "{{ ansible_env['PYTHONPATH'] | default('') }}:{{ python_user_site }}"
      community.docker.docker_image:
        name: "{{ item['name'] }}"
        source: pull
      loop: "{{ containers }}"
  become: true
```

---

```yaml
- name: Ensure pi user is added to the docker group.
  ansible.builtin.user:
    name: pi
    groups: docker
    append: true

# reset_connection doesn't support conditionals.
- name: Reset connection so docker group is picked up.
  meta: reset_connection
```

---

```yaml
- name: Register gcloud config location
  ansible.builtin.shell: gcloud info --format="value(config.paths.active_config_path)"
  register: gcloud_active_config_path
```

---

```sh
--skip-tags {{ ansible_skip_tags | default(['never'], true) | join(',') }}
```