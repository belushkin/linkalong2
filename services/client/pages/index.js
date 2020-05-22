import Head from 'next/head'
import Link from 'next/link'
import Layout, { siteTitle } from '../components/layout'
import CreateForm from '../components/form'
import utilStyles from '../styles/utils.module.css'

import React from 'react';

import Links from '../components/links'

export default class Home extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            links: []
        };

        this.handleTextAdd = this.handleTextAdd.bind(this);
    }

    async componentDidMount() {
        const res = await fetch(`http://0.0.0.0:8080/api/list`)
        const data = await res.json()
        this.setState({ links: data })
    }

    handleTextAdd(text) {

        if (!text)
            return

        fetch(`http://0.0.0.0:8080/api/text`, {
            method: 'POST',
            body: JSON.stringify({'text':text}),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(res => res.json())
        .then(data => {
                this.setState(prevState => {
                    const newLinks = [data, ...prevState.links];

                    return {
                        links: newLinks
                    }
                });
        })
        .catch(err => console.error("Error:", err));
    }

    render() {
        return (
            <Layout home>
                <Head>
                    <title>{siteTitle}</title>
                </Head>
                <CreateForm
                    {...this.props}
                    {...this.state}
                    onAddLink={this.handleTextAdd}
                />
                <section className={`${utilStyles.headingMd} ${utilStyles.padding1px}`}>
                    <h2 className={`${utilStyles.headingLg} mt-10`}>Added texts</h2>
                    <Links
                        {...this.props}
                        {...this.state}
                    />
                </section>
            </Layout>
        )
    }
}
