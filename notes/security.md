# Security

## GPG keys

```bash
gpg --full-generate-key
gpg --export --armor <email>

gpg --list-secret-keys --keyid-format=long
gpg --armor --export <key_id>
```
