# Kindle Highlights

![showcase.gif](Showcase: How it works!)

Extracts all your Amazon Kindle highlights

## ToDos

- [x] Make the program more efficient
- [x] JSON Output
- [x] Remove keys of empty lists
- [X] Make executable
- [ ] Remove useless highlights on the kindle site
- [ ] Highlights from a specific book (search algo or regex)

Add this line at the end of your `.bashrc` file

```bash
export PATH=$PATH:/home/whoami/path/to/cloned/dir
```

### Bonus (for me!)

First use of ffmpeg program!

```bash
ffmpeg -ss 1 -t 3 -i 2022-05-25\ 18-23-47.mp4 -vf "fps=10,scale=640:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 showcase.gif
```
