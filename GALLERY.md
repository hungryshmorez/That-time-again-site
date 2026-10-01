# Gallery workflow

## Folder layout

```
public/
  gallery/
    al-and-sloppy/
    channel-86/
    that-time-again-records/
```

Each series page reads its matching folder directly from this public GitHub repository.

## Admin upload

Open the correct folder on GitHub and choose **Add file → Upload files**. Commit to `main`.
The website sees the new file automatically; no gallery code edit is required.

## Public submissions

Anyone with a GitHub account can open a **Gallery photo submission** issue and attach photos.

Nothing is published automatically from an untrusted issue. To approve a submission, a repository owner/member/collaborator comments:

```
/approve-gallery
```

The workflow downloads supported GitHub-hosted image attachments, places them in the selected series folder, commits them to `main`, comments on the issue, and closes it.

This moderation step prevents arbitrary public uploads from being published directly to the live gallery.
