# Grafana Dashboards Builder

A wrapper around [grafanalib](https://github.com/weaveworks/grafanalib) which simplifies generating multiple dashboards.

## Why?

Grafanalib is a fantastic tool which lets you generate Grafana dashboards from simple Python scripts. Unfortunately, it can only read single files as dashboard sources and doesn't have a concept of multiple output directories. Those limitations make it hard to provision an entire Grafana instance with many folders and multiple dashboard sources.

Grafana Dashboard Builder recursively finds all `.dashboard.py` files in a directory tree. It generates dashboards and places them in a one-level-deep subdirectories which represent [Grafana folders](https://grafana.com/docs/grafana/latest/reference/dashboard_folders/).

It's written with Kubernetes in mind so it also has an ability to parse filenames mounted from a flat ConfigMap and generate nested output directory structure (see [examples](#Examples) below).


## Installation

    pip install grafana-dashboards-builder


## Usage

    grafana-dashboards-builder [OPTIONS] INPUT_DIR [OUTPUT_DIR]

    INPUT_DIR is the directory tree with dashboard sources.

    OUTPUT_DIR is the directory where generated dashboards are placed (defaults to ./out).

    Options:
    --from-configmap  generate output directories based on a source files prefix and a '--' separator
    --help            Show this message and exit.


## Examples

### Sources in nested directories

Grafana supports only one level of depth for [folders](https://grafana.com/docs/grafana/latest/reference/dashboard_folders/). So even when dashboard sources are nested in multiple subdirectories the output dashboards will have only one parent directory (the most shallow one). 

Source dashboards that don't have any parent directory will be placed in the default `General` folder.

Given a following input directory tree:

    dashboards_in/
        main.dashboard.py
        kubernetes/
            workloads/
                pods.dashboard.py
                jobs.dashboard.py
            nodes/
                nodes.dashboard.py
        nginx/
            nginx_health.dashboard.py

A following output directory will be generated:

    dashboards_out/
        General/
            main.json
        Kubernetes/
            pods.json
            jobs.json
            nodes.json
        Nginx/
            nginx_health.json

### Sources in a ConfigMap

When running Grafana in Kubernetes cluster it's possible to run Grafana Dashboard Builder as a sidecar which loads dashboard sources from a ConfigMap and generates them into Grafana's `/var/lib/grafana/dashboards` directory.

ConfigMaps don't support nested directory structures so enable mapping dashboards to different folders we can prefix the sources filenames with a `folder--` prefix. When Grafana Dashboard Builder runs with `--from-configmap` flag it parses the filenames and generates output directories based on found prefixes. Filenames without a prefix will be placed in the default `General` folder.

Given a following input directory:

    dashboards_in/
        main.dashboard.py
        kubernetes--pods.dashboard.py
        kubernetes--jobs.dashboard.py
        nginx--nginx_health.dashboard.py
        
A following output directory will be generated:

    dashboards_out/
        General/
            main.json
        Kubernetes/
            pods.json
            jobs.json
        Nginx/
            nginx_health.json
