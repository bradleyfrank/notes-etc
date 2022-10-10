# Media

```sh
# convert GitHub Markdown to DokuWiki format
pandoc file.md -f gfm -t dokuwiki -o file.wiki

# remove password from PDF
pdftk /path/to/input.pdf input_pw PROMPT output /path/to/output.pdf

# encrypt/decrypt a file
openssl enc -aes-256-cbc -salt -in /path/to/input -out /path/to/output
openssl enc -d -aes-256-cbc -in /path/to/input -out /path/to/output

# converting documents with LibreOffice
soffice --headless --convert-to docx --outdir /tmp /path/to/doc
libreoffice --headless --convert-to epub /path/to/odt

# resize image by 50%
convert /path/to/file -resize 50% /path/to/output

# extract gif images
convert -coalesce file.gif out.png

# convert HEIC images
heif-convert "$f" ${f/%.HEIC/.JPG}

# convert webp images
ffmpeg -i "$f" "${f%.webp}.jpg"

# flac to mp3
flac -cd "$f" | lame -b 192 - "${f%.*}.mp3"

# mp4 to mp3
ffmpeg -i "$f" -b:a 192K -vn "${f%.*}.mp3"

# flac to m4a
ffmpeg -i "$f" -c:a alac "${f%.*}.m4a"

# m4a to flac
ffmpeg -i "$f" -f flac "${f%.*}.flac" -vsync 0

# mpg to mp4
ffmpeg -i input.mpg output.mp4
ffmpeg -i input.mp4 -vcodec libx264 -crf {18..24} output.mp4
ffmpeg -i input.mp4 -vcodec libx265 -crf {24..30} output.mp4

# m3u8 to mp4
ffmpeg -protocol_whitelist file,http,https,tcp,tls,crypto -i "$f" -c copy -bsf:a aac_adtstoasc "${f%.*}.mp4"
```

---

```sh
# rip blu-ray as decrypted backup
makemkvcon backup --decrypt disc:0 /path/to/folder

# rip blu-ray as mkv
makemkvcon mkv disc:0 all /path/to/folder

# convert ISO to mkv
makemkvcon mkv iso:/path/to/file.iso all /path/to/output

# merge mp4/mkv files
mkvmerge -o outfile.mkv infile_01.mp4 \+ infile_02.mp4 \+ infile_03.mp4
```