import Head from 'next/head'
import Link from 'next/link'
import { useRouter } from 'next/router'

import Layout, { siteTitle } from '../../components/layout'
import utilStyles from '../../styles/utils.module.css'


export default function Sentence({ sentenceData }) {

  const router = useRouter()
  const { id } = router.query

  return (
    <Layout>
      <Head>
        <title>{siteTitle}</title>
      </Head>
      <section className={`${utilStyles.headingMd}`}>Original sentence:</section>
        <section className={`${utilStyles.headingMd} ${utilStyles.padding1px}`}>
            <h2 className={utilStyles.headingLg}>{sentenceData.original.value}</h2>

            <ul className={`${utilStyles.list} mt-10`}>
                {sentenceData.search_result.map(({ sentence_id, sim, text, text_id }) => (
                    <li className={utilStyles.listItem} key={sentence_id}>
                        <Link href="/texts/[id]" as={`/texts/${text_id}`}>
                            <a>{text}</a>
                        </Link>
                        <span className={`ml-4`}>{sim}</span>
                    </li>
                ))}
            </ul>
        </section>
    </Layout>
  )
}

export async function getServerSideProps({ params }) {

    const res = await fetch(`http://nginx:8080/api/search/${params.id}`)
    const sentenceData = await res.json()

    return {
        props: { sentenceData }
    }
}
