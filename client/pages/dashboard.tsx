import { GetServerSideProps } from "next";

export default function Dashboard({ user }: { user: any }) {
  return (
    <div>
      <h1>Dashboard</h1>
      <pre>{JSON.stringify(user, null, 2)}</pre>
    </div>
  );
}

export const getServerSideProps: GetServerSideProps = async (context) => {
  const token = context.req.cookies["auth_token"];

  const res = await fetch("http://localhost:8000/protected", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!res.ok) {
    return {
      redirect: {
        destination: "/",
        permanent: false,
      },
    };
  }

  const data = await res.json();
  return { props: { user: data } };
};
