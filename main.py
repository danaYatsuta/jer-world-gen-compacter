import os, sys, json

if not os.path.isfile("world-gen.json"):
    sys.exit("world-gen.json not found.")

with open("world-gen.json") as f:
    raw_data = json.load(f)

processed_ores = []
result = []

for block_info in raw_data:
    block, distrib, dim = block_info["block"], block_info["distrib"], block_info["dim"]

    if (
        "ore" not in block[block.index(":") + 1 :]
        and block != "minecraft:ancient_debris"
        or block in processed_ores
        or block == "minecraft:spore_blossom"
    ):
        continue

    if "deepslate" in block:
        alternate_block = block.replace("deepslate_", "")
    else:
        alternate_block = block.replace(":", ":deepslate_")

    alternate_distrib = None

    for block_info2 in raw_data:
        if block_info2["block"] == alternate_block:
            alternate_distrib = block_info2["distrib"]
            break

    if alternate_distrib == None:
        result.append(block_info)
        continue

    distrib = [float(x[x.find(",") + 1 :]) for x in distrib.split(";")[:-1]]
    alternate_distrib = [
        float(x[x.find(",") + 1 :]) for x in alternate_distrib.split(";")[:-1]
    ]

    distrib_len = len(distrib)
    alternate_distrib_len = len(alternate_distrib)

    if distrib_len > alternate_distrib_len:
        for i in range(distrib_len - alternate_distrib_len):
            alternate_distrib.append(0)
    elif alternate_distrib_len > distrib_len:
        for i in range(alternate_distrib_len - distrib_len):
            distrib.append(0)

    combined_distrib = [x + y for x, y in zip(distrib, alternate_distrib)]
    combined_distrib = [str(f"{x:f}") for x in combined_distrib]

    for i in range(len(combined_distrib)):
        combined_distrib[i] = str(i) + "," + combined_distrib[i]

    combined_distrib = ";".join(combined_distrib) + ";"

    result.append(
        {"block": block, "distrib": combined_distrib, "silktouch": False, "dim": dim}
    )

    result.append(
        {
            "block": alternate_block,
            "distrib": combined_distrib,
            "silktouch": False,
            "dim": dim,
        }
    )

    processed_ores.extend([block, alternate_block])

with open("world-gen-compacted.json", "w") as f:
    f.write(json.dumps(result))
