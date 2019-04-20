from modules import budget_nitro, lounge_status, test_functions


def load_modules(client, debug=False):
    client.add_cog(budget_nitro.BudgetNitro(client))

    doorbot = lounge_status.LoungeDoorStatus(client)
    if not debug:
        doorbot.start_pi_listener()
    client.add_cog(doorbot)

    if debug:
        client.add_cog(test_functions.StatusTester(client))
