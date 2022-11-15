from consumer import Consumer


def main():
    consumers = []

    for i in range(10):
        consumer = Consumer()
        consumer.start()

        consumers.append(consumer)

    for consumer in consumers:
        consumer.join()


if __name__ == '__main__':
    main()
