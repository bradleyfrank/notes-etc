# Solutions

nVidia "night mode" fix for Linux:

> **`/etc/X11/xorg.conf.d/20-nvidia.conf`**
>
> ```ini
> Section "Device"
>   Option "UseNvKmsCompositionPipeline" "false"
> EndSection
> ```

---

macOS does not allow placing files directly in `sudoers.d/`, use `visudo` instead:

```sh
printf "%s ALL=(ALL) NOPASSWD: ALL\n" "$(id -un)" \
  | sudo VISUAL="tee" visudo -f /etc/sudoers.d/99-nopasswd
```

---

Firefox Google Meet bug: `media.setsinkid.enabled = true`

---

* `CAT6` is needed for 10Gbps up to 55m
* `CAT6A` is needed for 10Gbps up to 100m
* `CAT7` is not used for any standards compliant networking
* `CAT8` is "used" for 40Gbase-T up to 30 meters; in reality nobody uses `CAT8` they use fiber
