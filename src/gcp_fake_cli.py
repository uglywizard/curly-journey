import argparse

from google.cloud import pubsub_v1
from google.api_core.exceptions import GoogleAPICallError, RetryError


<<<<<<< HEAD
def list_topics(publisher, project_id):
    """Lists all Pub/Sub topics in the given project."""

    project_path = f"projects/{project_id}"

    for topic in publisher.list_topics(request={"project": project_path}):
        print(topic)


def create_topic(publisher, project_id, topic_id):
    """Create a new Pub/Sub topic."""

    topic_path = publisher.topic_path(project_id, topic_id)

    topic = publisher.create_topic(request={"name": topic_path})

    print(f"Created topic: {topic.name}")


def delete_topic(publisher, project_id, topic_id):
    """Deletes an existing Pub/Sub topic."""

    topic_path = publisher.topic_path(project_id, topic_id)

    publisher.delete_topic(request={"topic": topic_path})

    print("Topic deleted: {}".format(topic_path))


def create_subscription(subscriber, project_id, topic_id, subscription_id):
=======
def create_push_subscription(project_id, topic_id, subscription_id, endpoint):
    """Create a new push subscription on the given topic."""
    from google.cloud import pubsub_v1

    publisher = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    push_config = pubsub_v1.types.PushConfig(push_endpoint=endpoint)

    # Wrap the subscriber in a 'with' block to automatically call close() to
    # close the underlying gRPC channel when done.
    with subscriber:
        subscription = subscriber.create_subscription(
            request={
                "name": subscription_path,
                "topic": topic_path,
                "push_config": push_config,
            }
        )

    print(f"Push subscription created: {subscription}.")
    print(f"Endpoint for subscription is: {endpoint}")


def create_subscription(project_id, topic_id, subscription_id):
>>>>>>> Added push subscription creation option and flask api endpoint.
    """Create a new pull subscription on the given topic."""

    topic_path = subscriber.topic_path(project_id, topic_id)
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    # Wrap the subscriber in a 'with' block to automatically call close() to
    # close the underlying gRPC channel when done.
    with subscriber:
        subscription = subscriber.create_subscription(
            request={"name": subscription_path, "topic": topic_path}
        )

    print(f"Subscription created: {subscription}")


def detach_subscription(publisher, subscriber, project_id, subscription_id):
    """Detaches a subscription from a topic and drops all messages retained in it."""

    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    try:
        publisher.detach_subscription(request={"subscription": subscription_path})
    except (GoogleAPICallError, RetryError, ValueError, Exception) as err:
        print(err)

    subscription = subscriber.get_subscription(
        request={"subscription": subscription_path}
    )
    if subscription.detached:
        print(f"{subscription_path} is detached.")
    else:
        print(f"{subscription_path} is NOT detached.")


if __name__ == "__main__":
    publisher = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("project_id", help="Google Cloud project ID")

    subparsers = parser.add_subparsers(dest="command")

    list_topic_parser = subparsers.add_parser("list-topics", help=list_topics.__doc__)

    create_topic_parser = subparsers.add_parser(
        "create-topic", help=create_topic.__doc__
    )
    create_topic_parser.add_argument("topic_id")

    delete_topic_parser = subparsers.add_parser(
        "delete-topic", help=delete_topic.__doc__
    )
    delete_topic_parser.add_argument("topic_id")

    create_subscription_parser = subparsers.add_parser(
        "create-subscription",
        help=create_subscription.__doc__,
    )
    create_subscription_parser.add_argument("topic_id")
    create_subscription_parser.add_argument("subscription_id")

<<<<<<< HEAD
    detach_subscription_parser = subparsers.add_parser(
        "detach-subscription", help=detach_subscription.__doc__
    )
    detach_subscription_parser.add_argument("subscription_id")
=======
    create_push_subscription_parser = subparsers.add_parser(
        "create-push-subscription",
        help=create_push_subscription.__doc__,
    )
    create_push_subscription_parser.add_argument("topic_id")
    create_push_subscription_parser.add_argument("subscription_id")
    create_push_subscription_parser.add_argument("endpoint")
>>>>>>> Added push subscription creation option and flask api endpoint.

    args = parser.parse_args()

    if args.command == "create-topic":
        create_topic(publisher, args.project_id, args.topic_id)
    elif args.command == "create-subscription":
<<<<<<< HEAD
        create_subscription(
            subscriber, args.project_id, args.topic_id, args.subscription_id
        )
    elif args.command == "list-topics":
        list_topics(args.project_id)
    elif args.command == "delete-topic":
        delete_topic(publisher, args.project_id, args.topic_id)
    elif args.command == "detach-subscription":
        detach_subscription(
            publisher, subscriber, args.project_id, args.subscription_id
=======
        create_subscription(args.project_id, args.topic_id, args.subscription_id)
    elif args.command == "create-push-subscription":
        create_push_subscription(
            args.project_id, args.topic_id, args.subscription_id, args.endpoint
>>>>>>> Added push subscription creation option and flask api endpoint.
        )
