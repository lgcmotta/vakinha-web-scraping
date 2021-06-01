#!/usr/bin/env python

from lxml import html
import requests
import json
import argparse
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
    campaigns = []
    for index in range(len(campaigns_names)):
        campaigns.append({
            "nome": campaigns_names[index],
            "valorArrecadado": campaigns_values[index].replace('Arrecadado R$ ', ''),
            "meta": 0.00 if campaigns_goals[index] == 'Sem meta' else campaigns_goals[index].replace('Meta R$ ', '')
        })
    return campaigns


def extract_campaings(trees):
    campaigns = []
    for tree in trees:
        campaigns_names = get_campaigns_names(tree=tree)

        campaigns_values = get_campaigns_values(tree=tree)

        campaigns_goals = get_campaigns_goals(tree=tree)

        campaigns += append_campaings_per_page(campaigns_names=campaigns_names,
                                               campaigns_values=campaigns_values, campaigns_goals=campaigns_goals)
    return campaigns


def write_json_file(campaigns):
    with open('campanhas.json', 'w', encoding='utf-8') as file:
        file.truncate(0)
        file.write(json.dumps(campaigns, indent=2, ensure_ascii=False))
        file.close()


def map_to_csv_line(campaign):
    return '{name};{value};{goal}\n'.format(name=campaign["nome"], value=campaign['valorArrecadado'], goal=campaign['meta'])


def write_csv_file(campaigns):
    with open('campanhas.csv', 'w', encoding='utf-8') as file:
        file.truncate(0)
        header = 'Campanha;Valor Arrecadado;Meta\n'
        file.write(header)
        for campaign in campaigns:
            content = map_to_csv_line(campaign)
            file.write(content)
        file.close()


parser = argparse.ArgumentParser()

parser.add_argument(
    '--output', '-o', help="output type format, accept 'json' or 'csv'", type=str, default='csv')
parser.add_argument(
    '--pages', '-p', help="number of pages that will be scraped", type=int, default=1)

args = parser.parse_args()

output_type = args.output

if output_type != 'json' or output_type != 'csv':
    print(parser.print_help())
    sys.exit(1)

first_page = 1

total_pages = int(args.pages)

base_url = 'https://www.vakinha.com.br'

trees = get_html_trees()

campaigns = extract_campaings(trees=trees)

if output_type == 'json':
    print('Writing json file')
    write_json_file(campaigns=campaigns)
elif output_type == 'csv':
    print('Writing csv file')
    write_csv_file(campaigns=campaigns)

print('Vakinha campaigns were scraped and saved into the "campanhas.{extension}" file.'.format(
    extension=output_type))
