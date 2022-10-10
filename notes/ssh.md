# SSH

## Key Management

```sh
openssl rsa -text -noout -in /path/to/private/key # show key info
ssh-keygen -yf /path/to/private/key # restore a public key
ssh-keygen -lf /path/to/private/key # verify key
ssh-keygen -R <hostname> -f ~/.ssh/known_hosts # remove host
ssh-copy-id # install public key in server's authorized_keys file

eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa
```

## Tunneling

```sh
# tunnel a remote port available via the proxy;
# i.e. remote = DB and proxy = bastion
ssh -M -S <ctl_path> -fNL <local_port>:<remote_host>:<remote_port> <proxy_host>
ssh -S <ctl_path> -O check <proxy_host> # check status of tunnel
ssh -S <ctl_path> -O exit <proxy_host> # close the tunnel

# tunnel a port from local system through ssh connection
ssh -R <remote_port>:localhost:<local_port> <remote_host>
```

## Configs

Not really a script, but a `.ssh/config` to automatically deploy parts of my local cli environment to every server i connect to (if username and ip/hostname matches my rules). On first connect to a server, this sync all the dotfiles i want to a remote host and on subsequent connects, it updates the dotfiles. `%d` = User's home directory

```text
   Match Host 192.168.123.*,another-example.org,*.example.com User myusername,myotherusername
      ForwardAgent yes
      PermitLocalCommand yes
      LocalCommand rsync -L --exclude .netrwhist --exclude .git --exclude .config/iterm2/AppSupport/ --exclude .vim/bundle/youcompleteme/ -vRrlptze "ssh -o PermitLocalCommand=no" %d/./.screenrc %d/./.gitignore %d/./.bash_profile %d/./.ssh/git_ed25519.pub %d/./.ssh/authorized_keys %d/./.vimrc %d/./.zshrc %d/./.config/iterm2/ %d/./.vim/ %d/./bin/ %d/./.bash/ %r@%n:/home/%r
```

## GPG

```sh
gpg --full-generate-key
gpg --export --armor <email>
gpg --list-secret-keys --keyid-format=long
gpg --armor --export <key_id>
```