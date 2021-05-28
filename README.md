# Simple PUB/SUB pull subscription example

## Configuration

This project need gcloud emulator, then, before start anything there are
some steps to cover for a correct execution:

- Install and setup gcloud PUB/SUB emulator on your machine (as explained [here](https://cloud.google.com/pubsub/docs/emulator))
- As explained on gc docs, be sure to export the needed env vars:
  - `gcloud beta emulators pubsub env-init`
- Alternatively use `docker-compose -f docker-compose.yml up -d` to run a container with a google cloud pubsub emulator (env variables are already defined).


At this point we are good to go for the next steps:

- `poetry install` 
- `poetry shell`

Before run src/publisher.py or src/subscriber.py we need to create a fake topic and a fake subscription on the emulator:

- `python run src/cli.py -h project_id {create-topic|create-subscription|create-push-subscription|list-topics|delete-topic|detach-subscription}` 
  - project_id: mandatory, setted in gcloud emulator start step.
  - create-topic: require a 'topic_id' (example: 'example_topic') on the previously defined 'project_id' (example: 'example-pub-sub create-topic example-topic')
  - create-subscription: require a 'topic_id' (previously defined) and a 'subscription_id' for the topic (example: 'example-pub-sub create-subscription example-topic example-subscription) 
  - create-push-subscription: require a 'topic-id' (previously defined), a 'subscription_id' and a configured push endpoint (example: 'example-pub-sub create-push-subscription example-topic example-push-subscription http://url-to-endpoint)
  - list-topics: no additional arguments required, only 'project_id' (example: example-pub-sub list-topics)
  - delete-topic: require a 'topic_id' previously defined (example: example-pub-sub delete-topic example-topic)
  - detach-subscription: require a 'subscription_id' previously defined on a 'topic_id' (example: example-pub-sub detach-subscription example-subscription)

#### Example

```
poetry run python src/cli.py project_id create-topic topic_id
poetry run python src/cli.py project_id create-push-subscription topic_id subscription_id endpoint_url
```

Now is possible to emulate a pull subscription flow. `src/publisher.py` and `src/subscriber.py` need to run separately.

## Run scripts

After topic and subscription creation is possible to run scripts correctly. 

### Publisher

- `python src/publisher.py -h [-m MESSAGE] project_id topic_id`
  - project_id: previously defined project_id
  - topic_id: previously defined topic_id
  - message: custom message to publish (Default='Hello, World!')
  
### Subscriber

- `python src/subscriber -h project_id subscription_id sleep`
  - project_id: previously defined project_id
  - subscription_id: previously defined subscription_id
  - sleep: a integer value that mitigates while cycle execution while listening on topic subscription updates (Default=30)

### Flask push endpoint

- Add an env var with path to flask app path (example: FLASK_APP=path/to/flask/app)
- `flask run`
- Create a push subscription with the correct endpoint (with default config, example: http://localhost:5000/pubsub/push)
- Publish to topic.

Scripts run asynchronously as expected from gcloud PUB/SUB, if publisher has published something, subscriber will receieve all the 
messages in queue 'till that point in time (all messages are retained indefinitely in the emulator context, as stated [here](https://cloud.google.com/pubsub/docs/emulator#emulator_command-line_arguments)).

### Hints

To speed up export of env var you can create an .env file with this vars and source it when needed.
```
export FLASK_APP=src/api/main.py
export FLASK_ENV=development
```

## Closing notes

`src/subscriber.py`, **gcloud emulator** and **flask dev server** will run until terminated, then, when satisfied, exit manually from the cli (CTRL+C)
and clean the env vars (`unset PUBSUB_EMULATOR_HOST` and `unset GOOGLE_APPLICATION_CREDENTIALS`).
