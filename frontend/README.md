# Bike Shop Frontend

You can develop on the frontend without Docker.

Make sure you have npm installed. Then, to install dependencies run:

```sh
cd frontend
npm install
```

You can use `.env.example` as example to set up an env file, for the API URL, which can be used in the apiClient.ts.

You can run the dev server with:

```sh
npm run dev
```

You can build with:

```sh
npm run build
```

And you can run tests with:

```sh
npm run test
```

For code formatting and checks you can manually run:

```sh
npm run format
npm run lint
npm run type-check
```

Ideally, your editor should reformat on Save.
