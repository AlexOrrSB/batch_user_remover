## Sendbird Batch User Remover
This is used to remove users from a Sendbird group channel in small batches in the event this is required. This will remove all members from a channel and delete the channel. This is not supported and may delete more than you intend. Be careful!

The max batch size is 100.

Install the dependencies and replaces the variables in the following command then run:

`python channel_member_remover.py APP_ID API_TOKEN CHANNEL_URL BATCH_SIZE`