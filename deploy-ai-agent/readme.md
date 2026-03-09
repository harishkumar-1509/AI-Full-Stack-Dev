# Running the Application

This project uses Docker to provide a Node.js environment, so Node.js does not need to be installed locally on your machine.

Follow the steps below to initialize and deploy the application.

---

## 1. Start a Node environment using Docker

```bash
docker compose run node sh
```

**Explanation**

This command starts a temporary container using the Node image defined in `docker-compose.yml` and opens a shell inside it. This allows you to run Node.js and npm commands inside the container without installing Node.js on your local system.

---

## 2. Install the Vercel CLI

```bash
npm i -g vercel@latest
```

**Explanation**

This installs the Vercel Command Line Interface globally inside the container. The CLI is required to initialize, configure, and deploy applications to the Vercel platform.

---

## 3. Initialize the FastAPI project for Vercel

```bash
vc init fastapi
```

**Explanation**

This command configures the project to run a FastAPI application on Vercel. It generates the necessary configuration files so Vercel knows how to build and run the API.

---

## 4. Deploy the application

```bash
vc deploy
```

**Explanation**

This performs the initial deployment of the project to Vercel and links your local project with a Vercel project.

---

## 5. Add the OpenAI API Key as an environment variable

```bash
vc env add OPENAI_API_KEY
```

**Explanation**

This command adds the `OPENAI_API_KEY` as a secure environment variable in the Vercel project. This allows the deployed application to safely access the OpenAI API without exposing the key in the source code.

---

## 6. Redeploy the application

```bash
vc deploy
```

**Explanation**

After adding the environment variable, the application must be redeployed so the new configuration is applied. The updated deployment will now have access to the `OPENAI_API_KEY`.

---

## Summary

This workflow ensures that:

* Node.js runs inside a Docker container instead of being installed locally.
* The Vercel CLI is used to initialize and deploy the FastAPI application.
* Sensitive values like API keys are stored securely as environment variables in Vercel.
* The application is deployed and updated directly from the container environment.
