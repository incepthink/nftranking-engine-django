from genericpath import exists
from io import BytesIO
from itertools import count
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
import pandas as pd
import numpy as np
from .serializer import ProjectSerializer, ProjectMetaSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import os
import concurrent.futures
import requests
import json
from ast import literal_eval
import zipfile
# import StringIO
import time
from web3 import Web3, HTTPProvider

# Create your views here.

from .models import Project


w3 = Web3(HTTPProvider('https://rpc.ftm.tools'))

# if (not w3.isConnected()):
#     print("Not connected")
#     exit()


def rank_new_project(project_name, base_url, abi, address, total_count):
    out = []
    CONNECTIONS = 100

    TIMEOUT = 5000

    urls = []

    attributes = {}

    attributes_values = {}

    attributes_types = {}

    attributes_rarity = {}

    attributes_count = {}

    # left_and_right_same = {}

    # left_and_right_same_count = 0

    none_attributes = {}

    nfts = []

    id = 0

    count = 0

    true_count = total_count

    contractCaller = w3.eth.contract(address=address, abi=abi)

    for i in range(1, true_count + 1):
        # print('Page:', i)
        url = base_url + str(
            i)
        urls.append(url)

    def load_url(url, timeout):
        try:
            r = requests.get(url, timeout=timeout)
            data = json.loads(r.text)
            global id

            name = data['name']

            id_local = name.split('#')[-1]

            # try:
            print(id_local)

            contractCaller.functions.ownerOf(int(id_local)).call()
            # except Exception as e:
            # continue

            nfts.append([data['name'], data['attributes'], data['image'], 0])

            attributes_count[len(data['attributes'])] = attributes_count[len(
                data['attributes'])] + 1 if len(
                    data['attributes']) in attributes_count else 1

            # left_item = None
            # right_item = None
            for attribute in data['attributes']:

                # if attribute['trait_type'] == 'Left Item':
                #     left_item = attribute['value']

                # if attribute['trait_type'] == 'Right Item':
                #     right_item = attribute['value']

                attributes_values[attribute['value'] + ' ' +
                                  attribute['trait_type']] = attributes_values[
                    attribute['value'] + ' ' +
                    attribute['trait_type']] + 1 if (
                    attribute['value'] + ' ' +
                    attribute['trait_type']
                ) in attributes_values else 1
                attributes_types[attribute['trait_type']] = attributes_types[
                    attribute['trait_type']] + 1 if attribute[
                        'trait_type'] in attributes_types else 1

                if attribute['trait_type'] in attributes:
                    attributes[attribute['trait_type']].add(attribute['value'])
                else:
                    attributes[attribute['trait_type']] = set()
                    attributes[attribute['trait_type']].add(attribute['value'])

            # if left_item == right_item:

            #     nonlocal left_and_right_same
            #     nonlocal left_and_right_same_count
            #     left_and_right_same[data['name']] = left_item
            #     left_and_right_same_count = left_and_right_same_count + 1

            # global count
            nonlocal count
            count = count + 1

        except Exception as e:
            print(e, "Over here")

    with concurrent.futures.ThreadPoolExecutor(
            max_workers=CONNECTIONS) as executor:
        future_to_url = (executor.submit(load_url, url, TIMEOUT)
                         for url in urls)
        time1 = time.time()
        for future in concurrent.futures.as_completed(future_to_url):
            try:
                data = future.result()
            except Exception as exc:
                data = str(type(exc))
            finally:
                out.append(data)

                print(str(len(out)), end="\r")

        time2 = time.time()

    print(f'Took {time2-time1:.2f} s')
    nft_df = pd.DataFrame(nfts,
                          columns=['name', 'attributes', 'image', 'rarity score'])

    #  drop the first column
    # nft_df = nft_df.drop(nft_df.columns[0], axis=1)

    # nft_df.reset_index(inplace=True)

    # nft_df.set_index('index', inplace=True)

    # print(nft_df)

    for key, value in attributes_count.items():
        rarity_of_count = value / count
        attributes_rarity['count ' + str(key)] = rarity_of_count

    for attribute in attributes:
        # print(attribute, attributes[attribute], attributes_types[attribute],
        #   "xxxx")

        count_for_no_value = count - attributes_types[attribute]

        # print(count_for_no_value)
        # attributes[attribute].add('No Value')

        for value in attributes[attribute]:
            # print(value, attributes_values[value])
            rarity = attributes_types[attribute] / attributes_values[value + ' ' +
                                                                     attribute]
            # print(rarity)
            attributes_rarity[value + ' ' + attribute] = rarity

        attributes_rarity[
            'None' + ' ' +
            attribute] = count / count_for_no_value if count_for_no_value != 0 else 0

        attributes[attribute].add('None')

        # none_attributes[attribute] = 'None'

    for nft in nfts:
        # print(nft)
        total_rarity = 0
        for attribute in attributes:
            found_flag = False

            for atr in nft[1]:
                if (atr['trait_type'] == attribute):
                    #    print("found")
                    found_flag = True

            if found_flag == False:
                # print("not found",attribute)

                total_rarity += attributes_rarity['None' +
                                                  ' ' + atr['trait_type']]
                #  add the rarity of the attribute to nft in df
                nft[1].append({'trait_type': attribute, 'value': 'None'})

        for x in nft[1]:
            # print(x)
            total_rarity += attributes_rarity[x['value'] +
                                              ' ' + x['trait_type']]

            #  check if attribute exits inside nft[1] 'trait_type'

            # if attribute in nft[1]:
            #     total_rarity += attributes_rarity[nft[1][attribute]['value'] + ' ' +
            #                                      attribute]
            # else:
            #     total_rarity += attributes_rarity['None' + ' ' + attribute]

        count_rarity = 'count ' + str(len(nft[1]))

        total_rarity += attributes_rarity[count_rarity] if count_rarity in attributes_rarity else 0

        nft[3] = total_rarity

        name = nft[0]

        # if (name in left_and_right_same):
        #     total_rarity += count / left_and_right_same_count
        #     # add the rarity of the attribute to nft in df
        #     nft[1].append({'trait_type': 'Left Right Same', 'value': True})
        # else:
        #     nft[1].append({'trait_type': 'Left Right Same', 'value': False})

        nft[3] = total_rarity

    # added Left Right Same in attribute lists

    # add none attributes to attributes list

    # attributes.update(none_attributes)

    print(attributes_rarity)

    print(attributes_types)

    nft_df = pd.DataFrame(nfts,
                          columns=['name', 'attributes', 'image', 'rarity score'])

    nft_df.sort_values(by=['rarity score'], ascending=False, inplace=True)

    nft_df.reset_index(inplace=True)

    nft_df.drop(nft_df.columns[0], axis=1, inplace=True)

    nft_df['rank'] = nft_df.index + 1

    nft_df.to_csv('rank_engine/engine_api/data/' +
                  project_name+'/ranks.csv', index=False)

    #  save all the trait types to a csv with multiplier set to 1 for each

    # print(attributes)

    # print(attributes['Race'])

    attributes_types_df = pd.DataFrame(
        [], columns=['trait_type', 'multiplier'])

    for x in attributes_types:
        attributes_types_df = attributes_types_df.append(
            {
                'trait_type': x,
                'multiplier': 1
            }, ignore_index=True)

    # attributes_types_df = attributes_types_df.append(
    #     {
    #         'trait_type': 'Left Right Same',
    #         'multiplier': 1
    #     }, ignore_index=True)

    print(attributes_types_df)

    # save attributes_types_df to csv sheet 2

    attributes_types_df.to_csv('rank_engine/engine_api/data/' +
                               project_name+'/attributes_types_meta.csv', index=False)

    # save all attributes value with multipler and trait type

    attributes_values_df = pd.DataFrame(
        [], columns=['trait_type', 'value', 'multiplier', 'rarity'])

    for x in attributes:
        for y in attributes[x]:

            rarity = attributes_rarity[y + ' ' + x]

            attributes_values_df = attributes_values_df.append(
                {
                    'trait_type': x,
                    'value': y,
                    'multiplier': 1,
                    'rarity': rarity
                },
                ignore_index=True)

    # attributes_values_df = attributes_values_df.append(
    #     {
    #         'trait_type': 'Left Right Same',
    #         'value': 'None',
    #         'multiplier': 1,
    #         'rarity': 0
    #     },
    #     ignore_index=True)

    # attributes_values_df = attributes_values_df.append(
    #     {
    #         'trait_type': 'Left Right Same',
    #         'value': True,
    #         'multiplier': 1,
    #         'rarity': count / left_and_right_same_count if left_and_right_same_count != 0 else 0
    #     },
    #     ignore_index=True)

    print(attributes_values_df)

    attributes_values_df.to_csv(
        'rank_engine/engine_api/data/' +
        project_name+'/attributes_values_meta.csv', index=False)


def recompute(project_name):

    nft_df = pd.read_csv('rank_engine/engine_api/data/' +
                         project_name+'/ranks.csv')

    attribute_type_df = pd.read_csv('rank_engine/engine_api/data/' +
                                    project_name+'/attributes_types_meta.csv')

    attribute_values_df = pd.read_csv('rank_engine/engine_api/data/' +
                                      project_name+'/attributes_values_meta.csv')

    attributes = {}

    attributes_values = {}

    attributes_types = {}

    attributes_rarity = {}

    attributes_count = {}

    left_and_right_same = {}

    left_and_right_same_count = 0

    nfts = []

    # get all the nfts into nft list

    for index, row in nft_df.iterrows():

        attributes_temp = literal_eval(row['attributes'])

        nfts.append(
            [row['name'], attributes_temp, row['image'], row['rarity score']])

    for index, row in attribute_type_df.iterrows():

        attributes_types[row['trait_type']] = row['multiplier']

    for index, row in attribute_values_df.iterrows():

        attribute_mutliplier = float(attributes_types[row['trait_type']]) if row[
            'trait_type'] in attributes_types and row['value'] != 'None' else 1

        attributes_rarity[
            str(row['trait_type'] + '_' + str(row['value'])
                )] = row['rarity'] * attribute_mutliplier * row['multiplier']

    for index, row in nft_df.iterrows():

        attributes_temp = literal_eval(row['attributes'])

        total_rarity = 0

        for attribute in attributes_temp:
            search_key = str(attribute['trait_type'] + '_' +
                             str(attribute['value']))

            if search_key in attributes_rarity:

                total_rarity += attributes_rarity[search_key]

        if (total_rarity == 0):
            continue

        nft_df.at[index, 'rarity score'] = total_rarity

    nft_df.sort_values(by=['rarity score'], inplace=True, ascending=False)

    nft_df.reset_index(drop=True, inplace=True)

    nft_df['rank'] = nft_df.index + 1

# nft_df.drop(columns=['index'], inplace=True)


class ProjectList(APIView):
    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():

            if(not Project.objects.filter(name=request.data['name']).exists()):
                serializer.save()
            #     print("already exists", request.data['name'])
            #     # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            # else:
            if not os.path.exists('rank_engine/engine_api/data/' + request.data['name']):
                os.makedirs('rank_engine/engine_api/data/' +
                            request.data['name'])

            # print(request.data['ipfs'])

            rank_new_project(
                request.data['name'], request.data['ipfs'], request.data['abi'], request.data['address'], request.data['count'])

           
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        project = self.get_object(pk)
        project.delete()

        os.system('rm -rf rank_engine/engine_api/data/' + project.name)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            name = request.data['name']
            recompute(name)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProjectMeta(APIView):

    def get(self, request, project_name):

        # name = request.query_params.get('project_name')

        # # get the csv file from data for attributes
        attributes_df = pd.read_csv('rank_engine/engine_api/data/' +
                                    project_name+'/attributes_types_meta.csv')

        # send all the attributes to the front end

        attributes_list = []

        for index, row in attributes_df.iterrows():
            attributes_list.append([row['trait_type'], row['multiplier']])

        return Response(attributes_list, status=status.HTTP_201_CREATED)

    def put(self, request, project_name):

        # change the multiplier of the attribute

        attributes_df = pd.read_csv('rank_engine/engine_api/data/' +
                                    project_name+'/attributes_types_meta.csv')

        attribute_to_change = request.data['attribute']

        multiplier = request.data['multiplier']

        attributes_df.loc[attributes_df['trait_type'] ==
                          attribute_to_change, 'multiplier'] = multiplier

        attributes_df.to_csv(
            'rank_engine/engine_api/data/' +
            project_name+'/attributes_types_meta.csv', index=False)

        return Response(status=status.HTTP_201_CREATED)


class ProjectAttributes(APIView):

    def get(self, request, project_name):

        # name = request.query_params.get('project_name')

        # # get the csv file from data for attributes
        attributes_df = pd.read_csv('rank_engine/engine_api/data/' +
                                    project_name+'/attributes_values_meta.csv')

        # send all the attributes to the front end

        attributes_df.fillna('None', inplace=True)

        attributes_list = []

        for index, row in attributes_df.iterrows():
            attributes_list.append(
                [row['trait_type'], row['value'], row['multiplier'], row['rarity']])

        return Response(attributes_list, status=status.HTTP_201_CREATED)

    def put(self, request, project_name):

        # change the multiplier of the attribute

        attributes_df = pd.read_csv('rank_engine/engine_api/data/' +
                                    project_name+'/attributes_values_meta.csv')

        attribute_to_change = request.data['attribute']

        value = request.data['value']

        attributes_df.loc[attributes_df['trait_type'] ==
                          attribute_to_change, 'value'] = value

        attributes_df.to_csv(
            'rank_engine/engine_api/data/' +
            project_name+'/attributes_values_meta.csv', index=False)

        return Response(status=status.HTTP_201_CREATED)


class ProjectRanks(APIView):

    def get(self, request, project_name):

        # name = request.query_params.get('project_name')

        # # get the csv file from data for attributes
        ranks_df = pd.read_csv('rank_engine/engine_api/data/' +
                               project_name+'/ranks.csv')

        # send all the attributes to the front end

        ranks_list = []

        for index, row in ranks_df.iterrows():
            ranks_list.append([row['rank'], row['name'], row['rarity score']])

        offset = request.query_params.get('offset') or 0

        limit = request.query_params.get('limit') or 10

        return Response(ranks_list[int(offset):int(offset)+int(limit)], status=status.HTTP_201_CREATED)

# class to download the csv file


class CSVDownloader(APIView):

    def get(self, request, project_name):

        # name = request.query_params.get('project_name')

        # # get the csv file from data for attributes
        ranks_df = pd.read_csv('rank_engine/engine_api/data/' +
                               project_name+'/ranks.csv')

        file_paths = ['rank_engine/engine_api/data/' + project_name+'/ranks.csv',
                      'rank_engine/engine_api/data/' + project_name+'/attributes_values_meta.csv',
                      'rank_engine/engine_api/data/' + project_name+'/attributes_types_meta.csv']

        zip_subdir = project_name

        zip_filename = "%s.zip" % zip_subdir

        s = BytesIO()

        zf = zipfile.ZipFile(s, "w")

        for fpath in file_paths:
            fdir, fname = os.path.split(fpath)
            zip_path = os.path.join(zip_subdir, fname)

            zf.write(fpath, zip_path)

        zf.close()

        resp = HttpResponse(
            s.getvalue(), content_type="application/x-zip-compressed")

        resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

        return resp

        raise Http404

        # send all the attributes to the front end
