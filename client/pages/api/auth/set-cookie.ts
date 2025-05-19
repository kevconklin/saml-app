import type { NextApiRequest, NextApiResponse } from "next";

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  const token = req.query.token as string;
  if (!token) {
    return res.status(400).send("Missing token");
  }

  res.setHeader("Set-Cookie", `auth_token=${token}; Path=/; HttpOnly`);
  res.redirect("/dashboard");
}
