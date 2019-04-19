from modules import budget_nitro


def load_modules(client, debug=False):
    client.add_cog(budget_nitro.BudgetNitro(client))

    pass
