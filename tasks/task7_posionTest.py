def designWineTests(testers: int):
    barrels = 1000

    # Check if the number of testers is sufficient
    if 2 ** testers < barrels:
        return False, None, None

    # Step 1: Build the testing schedule
    schedule = {}

    for tester in range(testers):
        schedule[tester] = []

        for barrel in range(barrels):
            # Check if this tester's bit is 1
            if (barrel >> tester) & 1:
                schedule[tester].append(barrel)

    # Step 2: Build the decoder
    def decoder(results):
        poisoned_barrel = 0

        for tester in range(testers):
            if results[tester] == 1:  # Tester died
                poisoned_barrel |= (1 << tester)

        return poisoned_barrel

    return True, schedule, decoder
