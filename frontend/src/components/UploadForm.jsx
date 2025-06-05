import React, { useState } from 'react';
import axios from 'axios';
import { toast } from 'react-toastify';

const UploadForm = ({ onProductAdded }) => {
  const [formData, setFormData] = useState({
    name: '',
    url: '',
    target_price: '',
    platform: 'generic'
  });
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    const toastId = toast.loading("Adding product and fetching initial data...");

    try {
      const productData = {
        ...formData,
        target_price: formData.target_price ? parseFloat(formData.target_price) : null
      };

      const response = await axios.post('http://localhost:8000/api/v1/products/', productData);
      
      toast.update(toastId, {
        render: "Product added successfully!",
        type: "success",
        isLoading: false,
        autoClose: 3000
      });

      setFormData({
        name: '',
        url: '',
        target_price: '',
        platform: 'generic'
      });

      if (onProductAdded) {
        onProductAdded(response.data);
      }

    } catch (error) {
      toast.update(toastId, {
        render: error.response?.data?.detail || "Failed to add product",
        type: "error",
        isLoading: false,
        autoClose: 3000
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4 text-gray-800">Track New Product</h2>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Product Name
          </label>
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter product name"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Product URL
          </label>
          <input
            type="url"
            name="url"
            value={formData.url}
            onChange={handleChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="https://example.com/product"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Target Price (Optional)
          </label>
          <input
            type="number"
            step="0.01"
            name="target_price"
            value={formData.target_price}
            onChange={handleChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="0.00"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Platform
          </label>
          <select
            name="platform"
            value={formData.platform}
            onChange={handleChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="generic">Generic</option>
            <option value="amazon">Amazon</option>
            <option value="ebay">eBay</option>
          </select>
        </div>

        <button
          type="submit"
          disabled={isLoading}
          className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition duration-200"
        >
          {isLoading ? 'Adding Product...' : 'Add Product'}
        </button>
      </form>
    </div>
  );
};

export default UploadForm;
