API routes for the server:

- /admin : For all the managment of server and api routes. Use the superuser account to access this route.

- /api : Access all the api functionalites of the server.

  - /api/projects/ [Get] : Get all the projects of the server saved in SQLite.
  - /api/projects/ [Post] : Add a new project to the server.

    <!-- table for post request  -->

    Request body
    <table>
        <tr>
            <th>Name</th>
            <th>Description</th>
            <th>Type</th>
            <th>Required</th>
        </tr>
        <tr>
        <td>Name</td>
        <td>The name of the project</td>
        <td>String</td>
        <td>True</td>
        </tr>
        <tr>
        <td>Description</td>
        <td>The description of the project</td>
        <td>String</td>
        <td>True</td>
        </tr>
        <tr>
        <td>ABI</td>
        <td>The ABI of the project</td>
        <td>String</td>
        <td>(Required for owner check)</td>
        </tr>
        <tr>
        <td>ipfs</td>
        <td>The ipfs hash of the project</td>
        <td>String</td>
        <td>True</td>
        </tr>
        <tr>
        <td>address</td>
        <td>The address of the smart contract</td>
        <td>String</td>
        <td>True</td>
        </tr>
        <tr>
        <td>Total Count</td>
        <td>The total count of the nfts in the  project</td>
        <td>INT</td>
        <td>True</td>
        </tr>
    </table>

    - /api/projects/ [Put] : Update a project of the server and recompute the ranks as per the multipliers set.

    - /api/projects/ [Delete] : Delete a project of the server ( provide id of the project in the data).

    - /api/projects/ranks/<str:project_name>/ [Get] : Get the ranks of the project. Query parameters: offset: (default 0) and limit: (default 10)

    - api/projects/meta/<str:project_name>/ [Get] : Get the meta data of the project for the attribute type. (multipler)

    - api/projects/meta/<str:project_name>/ [Put] : Update the meta data of the project for the attribute type. (multiplier)

    - api/projects/attributes/<str:project_name>/ [Get] : Get the attributes of the project. (multiplier and rarity value)

    - api/projects/attributes/<str:project_name>/ [Put] : Update the attributes of the project. (multiplier and rarity value)

    - api/projects/download/<str:project_name>/ [Get] : Download the project's csv file set in a zip file with the name of the project.