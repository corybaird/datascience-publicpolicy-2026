NATIONALITY_GROUPS = {
    "domestic": ["GB"],
    "chinese": ["CN"],
    "indian": ["IN"],
}


def bucket_nationality(label):
    if label is None:
        return None
    for bucket, labels in NATIONALITY_GROUPS.items():
        if label in labels:
            return bucket
    return "other_foreign"