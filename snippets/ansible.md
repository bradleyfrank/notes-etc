# Ansible

## macOS Python Version

```yaml
- name: get Python version
  ansible.builtin.command:
    cmd: brew info python --json
  register: cmd_brew_info_python
- name: show Python version
  ansible.builtin.debug:
    msg: "{{ cmd_brew_info_python['stdout'] | from_json | community.general.json_query('[].versions.stable') }}"
```

## Disks

```yaml
---

- name: Print disk info
  hosts: all
  tasks:
    - name: Print disk information
      loop: "{{ ansible_devices | dict2items }}"
      loop_control:
        label: "{{ item['key'] }}"
      when: item['value']['wwn'] is defined
      ansible.builtin.debug:
        msg: "/dev/{{ item['key'] }}: wwn-{{ item['value']['wwn'] }} ({{ item['value']['size'] }})"
```

## Docker

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

## Tags

```sh
--skip-tags {{ ansible_skip_tags | default(['never'], true) | join(',') }}
```

```sh
# convert Ansible tags into selectable list
ansible-playbook playbook.yml --list-tags \
  | sed -rn 's/^\s+TASK\sTAGS:\s\[(.*)\]$/\1/p' \
  | sed 's/, /\n/g' \
  | fzf --multi --ansi -i -1 --height=50% --reverse -0 --border \
  | xargs \
  | tr ' ' ','
```

## Copying Files

```yaml
- name: Copy SSH keys
  ansible.builtin.copy:
    src: "{{ item['src'] }}"
    dest: "{{ ansible_user_dir }}/.ssh"
    mode: "{{ '0644' if 'pub' in item['src'] | basename else '0600' }}"
  loop: "{{ lookup('community.general.filetree', 'ssh/') }}"
  loop_control:
    label: "{{ item['src'] | basename }}"
  when: manage_ssh_config and (item['src'] | basename != 'config')
```

## Setting Facts

```yaml
- name: Record new version of {{ name }}
  vars:
    existing_packages: "{{ github_package_versions | default({}) }}"
  set_fact:
    github_package_versions: "{{ existing_packages | combine({name: latest_release}) }}"
    cacheable: true
```

## Downloading

```yaml
- name: Install kubectl
  vars:
    url: https://storage.googleapis.com/kubernetes-release/release
    release: "{{ lookup('url', 'https://dl.k8s.io/release/stable.txt') }}"
    arch: "{{ 'amd64' if ansible_architecture == 'x86_64' else 'arm64' }}"
  ansible.builtin.get_url:
    url: "{{ url }}/{{ release }}/bin/{{ ansible_system | lower }}/{{ arch }}/kubectl"
    dest: "{{ ansible_user_dir }}/.local/bin/"
    mode: 0755
```

## Templating

```j2
{% for device in ansible_devices %}
{% if ansible_devices[device]['vendor'] %}
DEVICESCAN -a -s (S/../.././02|L/../../6/03) -o on -S on -n standby,q -m {{ email }}
{% endif %}
{% endfor %}
```
