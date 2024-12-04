def display_dict(dict, title=None):
    if title is None:
        pass
    else:
        print(title)
    for key, value in dict.items():
        print(f"\t- {key}: {value:.4f}")