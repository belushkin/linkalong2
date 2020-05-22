import Head from 'next/head'
import Link from 'next/link'
import Layout, { siteTitle } from '../components/layout'
import utilStyles from '../styles/utils.module.css'

export default function Home({ data }) {

  return (
    <Layout home>
      <Head>
        <title>{siteTitle}</title>
      </Head>
      <section className={utilStyles.headingMd}>…</section>
        <section className={`${utilStyles.headingMd} ${utilStyles.padding1px}`}>
            <h2 className={utilStyles.headingLg}>Blog</h2>
            <ul className={utilStyles.list}>
                {data.map(({ id, text }) => (
                    <li className={utilStyles.listItem} key={id}>
                        <Link href="/texts/[id]" as={`/texts/${id}`}>
                            <a>{text}</a>
                        </Link>
                    </li>
                ))}
            </ul>
        </section>
    </Layout>
  )
}

export async function getServerSideProps() {
  const res = await fetch(`http://nginx:8080/api/list`)
  const data = await res.json()

  return { props: { data } }
}
