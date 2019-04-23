from modules import budget_nitro, lounge_status, test_functions


def load_modules(client, use_raspi=True):
    # Load budget_nitro
    client.add_cog(budget_nitro.BudgetNitro(client))

    # Load lounge_status
    doorbot = lounge_status.LoungeDoorStatus(client)
    if use_raspi:
        doorbot.start_pi_listener()
    client.add_cog(doorbot)

    # Load test_functions
    if not use_raspi:
        client.add_cog(test_functions.StatusTester(client))
