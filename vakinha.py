#!/usr/bin/env python

from lxml import html
import requests
import json
import sys


def get_html_trees():
    trees = []
    for pageNumber in range(first_page, total_pages + 1):
        print('Getting content from page {page}'.format(page=pageNumber))
        page = requests.get(
            '{base_url}/vaquinhas/explore?page={page}'.format(base_url=base_url, page=pageNumber))
        tree = html.fromstring(page.content)
        trees.append(tree)
    return trees


def get_campaigns_names(tree):
    return tree.xpath(
        '//h3[@class="CampaignTitlestyles__H3-gbnzzd-0 jjEQQW"]/text()')


def get_campaigns_values(tree):
    return tree.xpath(
        '//div[@class="CampaignCardstyles__PledgedInfo-sc-1qyavwb-5 fSNTvh"]/text()')


def get_campaigns_goals(tree):
    return tree.xpath(
        '//div[@class="CampaignCardstyles__GoalInfo-sc-1qyavwb-6 kpnKMU"]/text()')


def append_campaings_per_page(campaigns_names, campaigns_values, campaigns_goals):
    for index in range(len(campaigns_names)):
        campaigns.append({
            "nome": campaigns_names[index],
            "valorArrecadado": campaigns_values[index].replace('Arrecadado R$ ', ''),
            "meta": 0.00 if campaigns_goals[index] == 'Sem meta' else campaigns_goals[index].replace('Meta R$ ', '')
        })


def extract_campaings(trees):
    for tree in trees:
        campaigns_names = get_campaigns_names(tree=tree)

        campaigns_values = get_campaigns_values(tree=tree)

        campaigns_goals = get_campaigns_goals(tree=tree)

        append_campaings_per_page(campaigns_names=campaigns_names,
                                  campaigns_values=campaigns_values, campaigns_goals=campaigns_goals)


def write_json_file():
    print('Writing json file')
    with open('campanhas.json', 'w', encoding='utf-8') as file:
        file.truncate(0)
        file.write(json.dumps(campaigns, indent=2, ensure_ascii=False))
        file.close()


def map_to_csv_line(campaign):
    return '{name};{value};{goal}\n'.format(name=campaign["nome"], value=campaign['valorArrecadado'], goal=campaign['meta'])


def write_csv_file():
    print('Writing csv file')
    with open('campanhas.csv', 'w', encoding='utf-8') as file:
        file.truncate(0)
        header = 'Campanha;Valor Arrecadado;Meta\n'
        file.write(header)
        for campaign in campaigns:
            content = map_to_csv_line(campaign)
            file.write(content)
        file.close()


output_type = sys.argv[1]

if not output_type:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)

first_page = 1

total_pages = int(sys.argv[2])

base_url = 'https://www.vakinha.com.br'

trees = get_html_trees()

campaigns = []

extract_campaings(trees=trees)

if output_type == 'json':
    write_json_file()
elif output_type == 'csv':
    write_csv_file()
