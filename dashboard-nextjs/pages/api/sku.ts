// Next.js API route support: https://nextjs.org/docs/api-routes/introduction

import axios, { AxiosError } from "axios";
import { NextApiRequest, NextApiResponse } from "next";

export default function (req: NextApiRequest, res: NextApiResponse) {
  axios.get(process.env.API_BASE_URL + "/get/sku").then(
    (data) => {
      res.status(200).json(data.data);
    },
    (err: AxiosError) => {
      res.status(503).json(err.message);
    }
  );
}
