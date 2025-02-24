This is a small Python script to compact output of [RegionScanner](https://github.com/RundownRhino/RegionScanner).

It removes all non-ore entries (assumes that ore blocks have "ore" in the name), and if an ore has a deepslate variant (assumes that it follows "modname:deepslate_ore_name" format), makes "distrib" value of both variants a sum of individual variants' "distrib" values.
