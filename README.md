# Simple PUB/SUB pull subscription example

## Configuration

This project need gcloud emulator, then, before start anything there are
some steps to cover for a correct execution:

- Install and setup gcloud PUB/SUB emulator on your machine (as explained [here](https://cloud.google.com/pubsub/docs/emulator))
- As explained on gc docs, be sure to export the needed env vars:
  - `gcloud beta emulators pubsub env-init`
- An IAM key json file is needed for the correct execution of the application (more on credentials creation [here](https://cloud.google.com/pubsub/docs/building-pubsub-messaging-system#create_service_account_credentials))
  - `export GOOGLE_APPLICATION_CREDENTIALS='/path/to/key/.json'`

At this point we are good to go for the next steps:

- `poetry install` 
- `poetry shell`

Before run src/publisher.py or src/subscriber.py we need to create a fake topic and a fake subscription on the emulator:

- `python run src/gcp_fake_cli.py -h project_id {create-topic|create-subscription}` 
  - project_id: mandatory, setted in gcloud emulator start step.
  - create-topic: require a 'topic_id' (example: 'example_topic') on the previously defined 'project_id' (example: 'example_pub_sub create-topic example_topic')
  - create-subscription: require a 'topic_id' (previously defined) and a 'subscription_id' for the topic (example: 'example_pub_sub create-subscription example_topic example_subscription) 

Now is possible to emulate a pull subscription flow. `src/publisher.py` and `src/subscriber.py` need to run separately.

## Run scripts

After topic and subscription creation is possible to run scripts correctly. 

### Publisher

- `python src/publisher.py -h [-m MESSAGE] project_id topic_id`
  
### Subscriber

- `python src/subscriber -h project_id subscription_id sleep`
  - project_id: previously defined project_id
  - subscription_id: previously defined subscription_id
  - sleep: a integer value that mitigates while cycle execution while listening on topic subscription updates (default=30)

Scripts run asynchronously as expected from gcloud PUB/SUB, if publisher has published something, subscriber will receieve all the 
messages in queue 'till that point in time (all messages are retained indefinitely in the emulator context, as stated [here](https://cloud.google.com/pubsub/docs/emulator#emulator_command-line_arguments)).

## Closing notes

`src/subscriber.py` and **gcloud emulator** will run until terminated, then, when satisfied, exit manually from the cli (CTRL+C)
and clean the env vars (`unset PUBSUB_EMULATOR_HOST` and `unset GOOGLE_APPLICATION_CREDENTIALS`).
