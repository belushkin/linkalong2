import React from 'react';
import { useFormik } from 'formik';

import Links from './links'

const CreateForm = ( {onAddLink} ) => {

    const formik = useFormik({
        initialValues: {
            text: '',
        },
        onSubmit: values => {
    //        onAddLink()
    //      alert(JSON.stringify(values, null, 2));
            onAddLink(values.text)
        },
    });


  return (
    <form onSubmit={formik.handleSubmit}>
      <textarea
        id="text"
        name="text"
        className="w-full h-64 resize border rounded focus:outline-none focus:shadow-outline block"
        onChange={formik.handleChange}
        value={formik.values.text}
      />
      <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline mt-10" type="submit">Submit</button>
    </form>
  );
};

export default CreateForm;
