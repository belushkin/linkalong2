import Head from 'next/head'
import Layout, { siteTitle } from '../components/layout'
import utilStyles from '../styles/utils.module.css'
import { getSortedPostsData } from '../lib/posts'

export default function Home({ data }) {
console.log(data)
  return (
    <Layout home>
      <Head>
        <title>{siteTitle}</title>
      </Head>
    </Layout>
  )
}

export async function getServerSideProps() {
  // Fetch data from external API
  const res = await fetch(`http://nginx:8080/api/list`)
  const data = await res.json()
  console.log('vnaxue')
  console.log(data)

  // Pass data to the page via props
  return { props: { data } }
}
