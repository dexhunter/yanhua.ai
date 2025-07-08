// functions/api/[[path]].js

import jsonData from "../../citations_data.json";

export const onRequestGet = async () => {
  return new Response(JSON.stringify(jsonData), {
    headers: {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*",
    },
  });
};