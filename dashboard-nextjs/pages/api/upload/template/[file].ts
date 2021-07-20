// Next.js API route support: https://nextjs.org/docs/api-routes/introduction

import { getIp } from "@/utils/helpers";
import axios, { AxiosError } from "axios";
import { NextApiRequest, NextApiResponse } from "next";
import formidable from "formidable";

export const config = {
  api: {
    bodyParser: false,
  },
};

export default async (req: NextApiRequest, res: NextApiResponse) => {
  const use_ip = getIp(req.headers.host);
  const baseUrl = "http://" + use_ip + req.url;
  console.log("baseUrl", req.url);
  console.log("baseUrl", baseUrl);

  const form = new formidable.IncomingForm();
  form.parse(req, (err, fields, files) => {
    console.log("api > form", { err, fields, files });
  });

  axios.post(baseUrl, form).then(
    (data) => {
      res.status(200).json({ status: "success", message: "success" });
    },
    (err: AxiosError) => {
      res.status(503).json(err.message);
    }
  );
};
