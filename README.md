Building off of the Data Harmonization effort from a while back, and now that the KCO is on the 7th floor is getting more integrated with the rest of the Xavier group, as well as several overlap between teams, it would be helpful to develop a “LIMS” for data centralization and standardization efforts. With the goal of providing easy and accessible information to those looking for file paths, metadata, etc.

To break it down into more digestible parts, from project conception to data it generally follows:

Intake (either of funding information, project specific goals, specimen metadata, etc.) 

↓

Processing (specimen sent to be sequenced, specimen receives treatment, record specific QC for each specimen during processing, etc.)

↓

Analysis (data is sent through analysis processes to produce numerical data)

Of course, there would be data entry at these steps (and even possible steps in between), which varies from person to person, but there still exists commonality in each group's respective recording system.

Central Organization Minimum

Based on three examples of information/columns tracked and different organizational structures used between the three groups:

Project - represents the overarching scientific or operational initiative that defines a unified biological or analytical objective. It serves as the top-level organizational entity under which all related experiments, samples, and analyses are grouped.

Sample - represents a discrete biological specimen: tissue, cell population, organoid, or derived material that physically or conceptually anchors all experimental measurements.

Experiment - defines a specific, reproducible protocol-driven operation applied to one or more samples to generate measurable data. It reflects the methodological layer between raw biology and analyzable data.

We should get on the same page for what each term means, and go forward recording/inserting existing data according to this schema.

The idea being that instead of having separate ways to also ingest information / data, kept it in different places, we should try to have a central location for data entry, with the flexibility to only track the data we’re concerned about, but also fit into a schema that works for the rest of the group. 

## Database Schema Overview

```mermaid
erDiagram

    PROJECTS ||--o{ SAMPLES : contains
    SAMPLES ||--o{ EXPERIMENTS : generates
    EXPERIMENTS ||--o{ RUN_EXPERIMENTS : participates_in
    SEQUENCING_RUNS ||--o{ RUN_EXPERIMENTS : includes
    RUN_EXPERIMENTS ||--o{ FILES : produces
    PROJECTS ||--o{ ID_CONCORDANCE : maps
    SAMPLES ||--o{ ID_CONCORDANCE : maps
    EXPERIMENTS ||--o{ ID_CONCORDANCE : maps
    SEQUENCING_RUNS ||--o{ ID_CONCORDANCE : maps

    PROJECTS {
        text id PK
        text name
        text description
        timestamp created_at
    }

    SAMPLES {
        text id PK
        text project_id FK
        text sample_name
        text organism
        text tissue
        timestamp created_at
    }

    EXPERIMENTS {
        text id PK
        text sample_id FK
        text assay_type
        text library_protocol
        date library_prep_date
        timestamp created_at
    }

    SEQUENCING_RUNS {
        text id PK
        text flowcell_id
        text machine
        date run_date
        timestamp created_at
    }

    RUN_EXPERIMENTS {
        text run_id FK
        text experiment_id FK
        text lane
        text index_sequence
    }

    FILES {
        int id PK
        text run_id FK
        text experiment_id FK
        text file_type
        text file_path
        text checksum
        timestamp created_at
    }

    ID_CONCORDANCE {
        int id PK
        text entity_type
        text internal_id
        text source_system
        text external_id
        timestamp created_at
    }

