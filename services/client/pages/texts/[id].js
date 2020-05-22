import Head from 'next/head'
import Link from 'next/link'
import { useRouter } from 'next/router'

import Layout, { siteTitle } from '../../components/layout'
import utilStyles from '../../styles/utils.module.css'


export default function Text({ textData }) {

  const router = useRouter()
  const { id } = router.query

  return (
    <Layout>
      <Head>
        <title>{siteTitle}</title>
      </Head>
      <section className={utilStyles.headingMd}>…</section>
        <section className={`${utilStyles.headingMd} ${utilStyles.padding1px}`}>
            <h2 className={utilStyles.headingLg}>Blog</h2>
            <ul className={utilStyles.list}>

                {textData.sentences.map(({ id, value }) => (
                    <li className={utilStyles.listItem} key={id}>
                        <Link href="/sentences/[id]" as={`/sentences/${id}`}>
                            <a>{value}</a>
                        </Link>
                    </li>
                ))}
            </ul>
        </section>
    </Layout>
  )
}


export async function getServerSideProps({ params }) {

    const res = await fetch(`http://nginx:8080/api/list/${params.id}`)
    const textData = await res.json()

    return {
        props: { textData }
    }
}
