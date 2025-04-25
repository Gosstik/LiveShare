import { Server, Response } from "miragejs";

import { getComments } from "./helpers";

import articles from "../assets/posts.json";
import { authUrl, postUrl } from "./urls";
import { stringify } from "uuid";

const get_post_timing = 500;
const get_comments_timing = 200;

export const errorsProbability = 0.2; // Emulate 500

new Server({
  routes() {
    this.namespace = "/api";
    // this.timing = 1000

    this.get(
      "/posts",
      () => {
        if (Math.random() < errorsProbability) {
          throw new Error("Something went wrong");
        }
        return articles;
      },
      { timing: get_post_timing }
    );

    this.get(
      "/comments/:postId",
      async (schema, request) => {
        if (Math.random() < errorsProbability) {
          return new Response(
            500,
            { some: "header" },
            { errors: ["something went wrong"] }
          );
        }

        const comments = await getComments(request.params.postId);
        return comments;
      },
      { timing: get_comments_timing }
    );

    // this.get(
    //   "/auth/oauth/yandex",
    //   async (schema, request) => {
    //     console.log(`request`);
    //     console.log(JSON.stringify(request));
    //     console.log(`schema`);
    //     console.log(JSON.stringify(schema));
    //     return {};
    //   }
    //   // { timing: get_comments_timing }
    // );

    // https://oauth.yandex.ru
    this.passthrough(
      "https://autofill.yandex.ru/version",
      "http://localhost:5000/auth/logged_in",
      "http://localhost:5000/api/auth/oauth/google",
      "http://localhost:5000/auth/token",
      "http://localhost:5000/user/info",
      "http://localhost:5000/auth/logout",
      // Django
      "http://localhost:8000/auth/oauth/google/url",
      "http://localhost:8000/auth/oauth/google/token/login",
      "http://localhost:8000/auth/login/check",
      "http://localhost:8000/auth/token/refresh",
      "http://localhost:8000/auth/logout",
      "http://localhost:8000/posts",
      "http://localhost:8000/comments/by-post/:postId",
    ); // oauth
  },
});
