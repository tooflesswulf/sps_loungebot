from modules import budget_nitro, lounge_status, test_functions


def load_modules(client, use_raspi=True):
    client.add_cog(budget_nitro.BudgetNitro(client))

    doorbot = lounge_status.LoungeDoorStatus(client)
    if use_raspi:
        doorbot.start_pi_listener()
    client.add_cog(doorbot)

    if not use_raspi:
        client.add_cog(test_functions.StatusTester(client))
