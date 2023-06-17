import React, { SyntheticEvent, useEffect, useState } from "react";
import { Navigate, useParams } from "react-router-dom";
import { Product } from "../interfaces/product";
import Wrapper from "./Wrapper";

const ProductsEdit = () => {
  const { id } = useParams<{ id: string }>(); // Access the "id" parameter from the URL

  const [title, setTitle] = useState('');
  const [image, setImage] = useState('');
  const [redirect, setRedirect] = useState(false);

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/products/${id}`);
        const product: Product = await response.json();
        setTitle(product.title);
        setImage(product.image);
      } catch (error) {
        console.log(error);
      }
    };

    fetchProduct();
  }, [id]);

  const submit = async (e: SyntheticEvent) => {
    e.preventDefault();
    try {
      await fetch(`http://localhost:8000/api/products/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title,
          image
        })
      });
      setRedirect(true);
    } catch (error) {
      console.log(error);
    }
  };

  if (redirect) {
    return <Navigate to={'/admin/products'} />;
  }

  return (
    <Wrapper>
      <form onSubmit={submit}>
        <div className="form-group">
          <label>Title</label>
          <input
            type="text"
            className="form-control"
            name="title"
            value={title}
            onChange={e => setTitle(e.target.value)}
          /><br /><br />
        </div>
        <div className="form-group">
          <label>Image</label>
          <input
            type="text"
            className="form-control"
            name="image"
            value={image}
            onChange={e => setImage(e.target.value)}
          /><br /><br />
        </div>
        <button className="btn btn-outline-secondary">Save</button>
      </form>
    </Wrapper>
  );
};

export default ProductsEdit;
