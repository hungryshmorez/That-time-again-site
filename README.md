# That Time Again Studios

Official site source for That Time Again Studios.

## Gallery folders

Upload series photos into `public/gallery/<series-slug>/`.

Current folders:
- `public/gallery/al-and-sloppy/`
- `public/gallery/channel-86/`
- `public/gallery/that-time-again-records/`

The build automatically regenerates `public/gallery-manifest.json`, so new images appear in the matching series gallery after the next deployment.

Public visitors can submit gallery images with the Gallery Photo issue form. A maintainer approves a submission by commenting `/approve-gallery` on the issue; GitHub Actions then imports the attached images into the correct gallery folder.
