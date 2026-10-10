import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configure publication style
sns.set_theme(style="whitegrid", font_scale=1.1)
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8

def normalize_columns(df):
    """Strip whitespace and map averaged/variant column names to standard headers."""
    df.columns = [str(col).strip() for col in df.columns]
    
    mapping = {}
    for col in df.columns:
        c_clean = col.lower().replace("_", "").replace(" ", "").replace("(", "").replace(")", "")
        if c_clean in ['cl', 'clavg', 'clmean', 'lift', 'liftcoefficient', 'clift']:
            mapping[col] = 'Cl'
        elif c_clean in ['cd', 'cdavg', 'cdmean', 'drag', 'dragcoefficient', 'cdrag']:
            mapping[col] = 'Cd'
        elif c_clean in ['mach', 'm', 'machnumber']:
            mapping[col] = 'Mach'
        elif c_clean in ['aoa', 'alpha', 'angle', 'angleofattack']:
            mapping[col] = 'AoA'
        elif c_clean in ['ld', 'l/d', 'cl/cd', 'lifttodrag']:
            mapping[col] = 'L/D'
            
    return df.rename(columns=mapping)

def process_and_plot_aerodynamics(csv_file="aerodynamic_results_analyzed.csv"):
    if not os.path.exists(csv_file):
        print(f"Error: '{csv_file}' not found in current directory.")
        return

    # Load dataset
    df = pd.read_csv(csv_file)
    
    # Standardize column headers
    df = normalize_columns(df)

    # Verify required force coefficient columns exist
    if 'Cl' not in df.columns or 'Cd' not in df.columns:
        print(f"Error: Could not automatically detect 'Cl' or 'Cd' columns.")
        print(f"Detected columns in file: {list(df.columns)}")
        return

    # Recompute or compute Lift-to-Drag ratio to ensure consistency
    df['L/D'] = df['Cl'] / df['Cd']

    # Sort rows by Mach and AoA to prevent line-crossing artifacts in plots
    if 'Mach' in df.columns and 'AoA' in df.columns:
        df = df.sort_values(by=['Mach', 'AoA']).reset_index(drop=True)

    # Save cleaned dataframe
    df.to_csv("aerodynamic_results_analyzed_clean.csv", index=False)

    mach_levels = sorted(df['Mach'].unique()) if 'Mach' in df.columns else []
    palette = sns.color_palette("tab10", len(mach_levels)) if mach_levels else None

    # ---------------------------------------------------------
    # 1. Lift Coefficient vs Angle of Attack (Cl vs AoA)
    # ---------------------------------------------------------
    if 'AoA' in df.columns and 'Cl' in df.columns:
        fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
        for idx, m in enumerate(mach_levels):
            m_data = df[df['Mach'] == m]
            ax.plot(m_data['AoA'], m_data['Cl'], marker='o', linewidth=2, 
                    label=f"Mach {m}", color=palette[idx])

        ax.set_title(r"Lift Curves ($C_L$ vs $\alpha$) Across Mach Regimes", fontsize=13, fontweight='bold', pad=12)
        ax.set_xlabel(r"Angle of Attack, $\alpha$ (°)", fontsize=11)
        ax.set_ylabel(r"Lift Coefficient ($C_L$)", fontsize=11)
        ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', frameon=True)
        plt.tight_layout()
        plt.savefig("Cl_vs_AoA_fixed.png", dpi=300)
        plt.close()

    # ---------------------------------------------------------
    # 2. Drag Polars (Cl vs Cd)
    # ---------------------------------------------------------
    if 'Cd' in df.columns and 'Cl' in df.columns:
        fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
        for idx, m in enumerate(mach_levels):
            m_data = df[df['Mach'] == m].sort_values(by='AoA' if 'AoA' in df.columns else 'Cd')
            ax.plot(m_data['Cd'], m_data['Cl'], marker='s', linewidth=2, 
                    label=f"Mach {m}", color=palette[idx])

        ax.set_title(r"Drag Polars ($C_L$ vs $C_D$)", fontsize=13, fontweight='bold', pad=12)
        ax.set_xlabel(r"Drag Coefficient ($C_D$)", fontsize=11)
        ax.set_ylabel(r"Lift Coefficient ($C_L$)", fontsize=11)
        ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', frameon=True)
        plt.tight_layout()
        plt.savefig("Drag_Polar_fixed.png", dpi=300)
        plt.close()

    # ---------------------------------------------------------
    # 3. Peak Efficiency Across Mach Regimes (Max L/D vs Mach)
    # ---------------------------------------------------------
    if 'Mach' in df.columns and 'L/D' in df.columns:
        summary = df.groupby('Mach')['L/D'].max().reset_index()
        summary.columns = ['Mach', 'Max_LD']

        fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)
        ax.plot(summary['Mach'], summary['Max_LD'], marker='D', color='darkred', 
                linewidth=2.2, markersize=6)

        # Highlight Transonic Dip Zone (M=0.8 to M=1.2)
        ax.axvspan(0.8, 1.2, color='gray', alpha=0.18, label='Transonic Dip Zone')

        ax.set_title(r"Aerodynamic Efficiency Across Speed Regimes", fontsize=13, fontweight='bold', pad=12)
        ax.set_xlabel("Mach Number", fontsize=11)
        ax.set_ylabel(r"Peak Lift-to-Drag Ratio $(L/D)_{\max}$", fontsize=11)
        ax.legend(loc='upper right')
        plt.tight_layout()
        plt.savefig("Max_LD_vs_Mach_fixed.png", dpi=300)
        plt.close()

        summary.to_csv("aerodynamic_results_summary.csv", index=False)

    print("Execution finished successfully! Updated plots saved as '_fixed.png'.")

if __name__ == "__main__":
    process_and_plot_aerodynamics()