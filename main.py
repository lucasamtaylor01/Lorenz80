import os
from pathlib import Path
import pandas as pd

from aux import simulations as sim
from aux import initial_conditions as ic
from aux import plot

BASE = Path(__file__).resolve().parent
DATADIR = BASE / "data"
DATADIR.mkdir(parents=True, exist_ok=True)

print("""==============================
>>  SELECT THE L80 MODEL  <<
==============================""")

print("1: PE Model")
print("2: BE Model")
print("3: QG Model")

model_type = int(input("\nSelected option: "))

if model_type == 1:
    df = sim.pe_simulate(ic.x0, ic.y0, ic.z0, ic.days)
    out_file = DATADIR / "pe_model.csv"
    df.to_csv(out_file, index=False)
    print("Process completed. File saved at:", out_file)
elif model_type == 2:
    df = sim.be_simulate(ic.y0, ic.days)
    out_file = DATADIR / "be_model.csv"
    df.to_csv(out_file, index=False)
    print("\nProcess completed. File saved at:", out_file)    
elif model_type == 3:
    df = sim.qg_simulate(ic.y0, ic.days)
    out_file = DATADIR / "qg_model.csv"
    df.to_csv(out_file, index=False)
    print("\nProcess completed. File saved at:", out_file)
else:
    print("Invalid option")
    exit()

data_cleaning = input("\nDo you want to remove 25% of the data? (y/n): ").strip().lower()
if data_cleaning == 'y':
    print("Cleaning data...")
    df = pd.read_csv(out_file)
    n_remove = int(len(df) * 0.25)
    filtered_df = df.iloc[n_remove:].copy()
    filtered_df.to_csv(out_file, index=False)
    df = filtered_df
    print(f"Cleaning completed. Removed ({n_remove/len(df)*100:.1f}% of data).")
elif data_cleaning == 'n':
    print("Data kept without changes.")
else:
    print("Invalid option. Data kept without changes.")

print("""\n==============================
>>  SELECT THE GRAPHIC OPTION  <<
==============================""")

while True:
    if model_type == 2 or model_type == 3:
        print("1: Projection y1 vs y2")
        print("2: Projection y1 vs y3")
        print("3: Projection y2 vs y3")
        print("4: Temporal evolution of y1")
        print("5: Temporal evolution of y2")
        print("6: Temporal evolution of y3")
        print("7: Stacked temporal evolution of y1, y2, y3")
        print("8: Generate all plots")

        graphic_option = int(input("\nChoose the graphic option: "))
        if graphic_option == 1:
            print(f"Plot saved at: {plot.plot_y1y2(df, model_type)}")
        elif graphic_option == 2:
            print(f"Plot saved at: {plot.plot_y1y3(df, model_type)}")
        elif graphic_option == 3:
            print(f"Plot saved at: {plot.plot_y2y3(df, model_type)}")
        elif graphic_option == 4:
            print(f"Plot saved at: {plot.plot_temporal(df, model_type, 'y1')}")
        elif graphic_option == 5:
            print(f"Plot saved at: {plot.plot_temporal(df, model_type, 'y2')}")
        elif graphic_option == 6:
            print(f"Plot saved at: {plot.plot_temporal(df, model_type, 'y3')}")
        elif graphic_option == 7:
            print(f"Plot saved at: {plot.temporal_evolution_y(df, model_type)}")
        elif graphic_option == 8:
            plot.generate_all_plots(df, model_type)
            print("Plots generated successfully.")
        else:
            print("Invalid option.")
            continue
    
    if model_type == 1:
        print("1: Projection y1 vs y2")
        print("2: Projection y1 vs y3")
        print("3: Projection y2 vs y3")
        print("4: Temporal evolution of y1, x1, z1")
        print("5: Stacked temporal evolution of y1, y2, y3")
        print("6: Generate all plots")

        graphic_option = int(input("Selected option: "))
        if graphic_option == 1:
            print(f"Plot saved at: {plot.plot_y1y2(df, model_type)}")
        elif graphic_option == 2:    
            print(f"Plot saved at: {plot.plot_y1y3(df, model_type)}")
        elif graphic_option == 3:    
            print(f"Plot saved at: {plot.plot_y2y3(df, model_type)}")
        elif graphic_option == 4:
            print(f"Plot saved at: {plot.plot_xyz_temporal(df, model_type)}")
        elif graphic_option == 5:
            print(f"Plot saved at: {plot.temporal_evolution_y(df, model_type)}")
        elif graphic_option == 6:
            plot.generate_all_plots(df, model_type)
            print("Plots generated successfully.")
        else:
            print("Invalid option.")
            continue
    
    exit_confirm = False
    while True:
        confirm = input("\nDo you want to continue with the plots? (y/n): ").strip().lower()
        if confirm == 'n':
            print("Closing the program.")
            exit_confirm = True
            break
        elif confirm == 'y':
            break
        else:
            print("Invalid option. Please enter 'y' or 'n'.")
    if exit_confirm:
        break

