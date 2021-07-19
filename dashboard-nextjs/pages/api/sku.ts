// Next.js API route support: https://nextjs.org/docs/api-routes/introduction

import { getIp } from "@/utils/helpers";
import axios, { AxiosError } from "axios";
import { NextApiRequest, NextApiResponse } from "next";

export default function (req: NextApiRequest, res: NextApiResponse) {
  const url = req.body.url;
  const use_ip = getIp(req.headers.host);
  const baseUrl = "http://" + use_ip + process.env.API_BASE_URL + url;
  axios.post(baseUrl).then(
    (data) => {
      res.status(200).json(data.data);
    },
    (err: AxiosError) => {
      res.status(503).json(err.message);
    }
  );
}
