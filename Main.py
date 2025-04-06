from SRC.Utils.UnitConverter import UnitConverter
import pandas as pd 


df = pd.DataFrame({
    "length_mm": [1000, 1500, 2000],
    "width_mm": [500, 750, 1000]
})

df["length_mm"] = UnitConverter.convert_vector(df["length_mm"] , "gravity", "m/s^2")
s= UnitConverter.convert_value(1, "gravity", "m/s^2")

print(df)
print(s)