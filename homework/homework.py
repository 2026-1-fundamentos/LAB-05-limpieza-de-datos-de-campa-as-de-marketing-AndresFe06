"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel


import pandas as pd
import os.path
import glob


def clean_campaign_data():

    def binarize_yes(value):
        return 1 if value == "yes" else 0

    def binarize_success(value):
        return 1 if value == "success" else 0

    def normalize_date(raw_date):
        parsed = pd.to_datetime(raw_date, format='%Y-%b-%d')
        return parsed.strftime('%Y-%m-%d')

    client_frames = []
    campaign_frames = []
    economics_frames = []

    for idx in range(10):
        source = pd.read_csv(
            f'files/input/bank-marketing-campaing-{idx}.csv.zip',
            compression='zip',
        )

        client_chunk = pd.DataFrame()
        client_chunk[["client_id", "age", "marital"]] = source[["client_id", "age", "marital"]]
        client_chunk["job"] = source["job"].str.replace(".", "").str.replace("-", "_")
        client_chunk["education"] = source["education"].str.replace(".", "_")
        client_chunk["education"] = client_chunk["education"].mask(
            client_chunk["education"] == "unknown", pd.NA
        )
        client_chunk["credit_default"] = source["credit_default"].apply(binarize_yes)
        client_chunk["mortgage"] = source["mortgage"].apply(binarize_yes)

        campaign_chunk = pd.DataFrame()
        campaign_chunk[
            ["client_id", "number_contacts", "contact_duration", "previous_campaign_contacts"]
        ] = source[
            ["client_id", "number_contacts", "contact_duration", "previous_campaign_contacts"]
        ]
        campaign_chunk["previous_outcome"] = source["previous_outcome"].apply(binarize_success)
        campaign_chunk["campaign_outcome"] = source["campaign_outcome"].apply(binarize_yes)
        campaign_chunk["last_contact_date"] = (
            "2022" + "-" + source["month"].astype(str) + "-" + source["day"].astype(str)
        )
        campaign_chunk["last_contact_date"] = campaign_chunk["last_contact_date"].apply(normalize_date)

        economics_chunk = pd.DataFrame()
        economics_chunk[["client_id", "cons_price_idx", "euribor_three_months"]] = source[
            ["client_id", "cons_price_idx", "euribor_three_months"]
        ]

        client_frames.append(client_chunk)
        campaign_frames.append(campaign_chunk)
        economics_frames.append(economics_chunk)

    client = pd.concat(client_frames, ignore_index=True)
    campaign = pd.concat(campaign_frames, ignore_index=True)
    economics = pd.concat(economics_frames, ignore_index=True)

    output_dir = "files/output/"
    if os.path.exists(output_dir):
        for file in glob.glob(f"{output_dir}*"):
            os.remove(file)
    else:
        os.makedirs(output_dir)

    client.to_csv(os.path.join(output_dir, "client.csv"), sep=",", index=False, header=True)
    campaign.to_csv(os.path.join(output_dir, "campaign.csv"), sep=",", index=False, header=True)
    economics.to_csv(os.path.join(output_dir, "economics.csv"), sep=",", index=False, header=True)
    return
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """

    return


if __name__ == "__main__":
    clean_campaign_data()
