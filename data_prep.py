import pandas as pd

# Files
files = {
    "rawdata/playstation/games.csv": "PS", 
    "rawdata/xbox/games.csv": "xbox", 
    "rawdata/steam/games.csv": "steam"
}

# Store the dfs
df_list = []

for file, platform in files.items():
    df = pd.read_csv(file)

    # Fill column based off which file path it was grabbed from
    df["console"] = platform  

    # Remove the platform column from playstation
    if "platform" in df.columns:
        df = df.drop(columns=["platform"])

    df_list.append(df)

# Combine the dataframes
combined_df = pd.concat(df_list, ignore_index=True)

# DEBUG: Check unique console values
print("Unique vals in console column:", combined_df["console"].unique())

# Create new platform columns
combined_df["PS"] = combined_df["console"].apply(lambda x: "Yes" if x == "PS" else "")
combined_df["Steam"] = combined_df["console"].apply(lambda x: "Yes" if x == "steam" else "")
combined_df["xBox"] = combined_df["console"].apply(lambda x: "Yes" if x == "xbox" else "")

# DEBUG: Check if platform assignment works
print("Checking PS column assignment:")
print(combined_df[["title", "console", "PS"]].head(10))

# Drop the console column
combined_df = combined_df.drop(columns=["console"])

# Group by game title
final_df = combined_df.groupby("title").agg({
    "gameid": "first",  # Just keep first game id. These don't translate between consoles.
    "developers": "first",
    "publishers": "first",
    "genres": "first",
    "supported_languages": "first",
    "release_date": "first",
    "PS": lambda x: "Yes" if "Yes" in x.values else "",
    "Steam": lambda x: "Yes" if "Yes" in x.values else "",
    "xBox": lambda x: "Yes" if "Yes" in x.values else ""
}).reset_index()


# Filter out gooner games
inappropriate_keywords = ["hentai", "furry", "porn", "sex", "nude", "naked", "erotic", "adult", "sexy", "nudity",
                          "sexual", "lewd", "ecchi", "harem", "yuri", "yaoi", "loli", "shota", "feet", "foot", "toe",
                          "underwear", "panties", "bra", "panty", "panties", "thong", "lingerie", "bikini", "swimsuit", "futanari"]

final_df = final_df[~final_df["title"].str.lower().str.contains('|'.join(inappropriate_keywords), na=False)]

# Keep only games that support English
final_df = final_df[final_df["supported_languages"].str.contains("English", case=False, na=False)]

# DEBUG: Check PS is filled
print("Final dataframe sample:")
print(final_df.head())

# Output save
final_df.to_csv("games_full.csv", index=False)

print("Good job buddy. You did it.")
