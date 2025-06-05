import React, { useState } from 'react';
import axios from 'axios';
import { toast } from 'react-toastify';

const ProductCard = ({ product, onProductUpdate, onProductDelete }) => {
  const [isUpdating, setIsUpdating] = useState(false);
  const [showPriceHistory, setShowPriceHistory] = useState(false);
  const [priceHistory, setPriceHistory] = useState([]);

  const checkPriceNow = async () => {
    setIsUpdating(true);
    const toastId = toast.loading("Checking current price...");

    try {
      await axios.post(`http://localhost:8000/api/v1/products/${product.id}/check-price`);
      
      // Fetch updated product data
      const response = await axios.get(`http://localhost:8000/api/v1/products/${product.id}`);
      
      toast.update(toastId, {
        render: "Price updated successfully!",
        type: "success",
        isLoading: false,
        autoClose: 3000
      });

      if (onProductUpdate) {
        onProductUpdate(response.data);
      }

    } catch (error) {
      toast.update(toastId, {
        render: "Failed to check price",
        type: "error",
        isLoading: false,
        autoClose: 3000
      });
    } finally {
      setIsUpdating(false);
    }
  };

  const fetchPriceHistory = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/api/v1/products/${product.id}/price-history`);
      setPriceHistory(response.data);
      setShowPriceHistory(true);
    } catch (error) {
      toast.error("Failed to fetch price history");
    }
  };

  const deleteProduct = async () => {
    if (window.confirm('Are you sure you want to delete this product?')) {
      try {
        await axios.delete(`http://localhost:8000/api/v1/products/${product.id}`);
        toast.success("Product deleted successfully");
        
        if (onProductDelete) {
          onProductDelete(product.id);
        }
      } catch (error) {
        toast.error("Failed to delete product");
      }
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      {product.image_url && (
        <img 
          src={product.image_url} 
          alt={product.name}
          className="w-full h-48 object-cover"
        />
      )}
      
      <div className="p-4">
        <h3 className="text-lg font-semibold text-gray-800 mb-2 line-clamp-2">
          {product.name}
        </h3>
        
        <div className="space-y-2 mb-4">
          <div className="flex justify-between">
            <span className="text-gray-600">Current Price:</span>
            <span className="font-bold text-green-600">
              ${product.current_price?.toFixed(2) || 'N/A'}
            </span>
          </div>
          
          {product.target_price && (
            <div className="flex justify-between">
              <span className="text-gray-600">Target Price:</span>
              <span className="font-semibold text-blue-600">
                ${product.target_price.toFixed(2)}
              </span>
            </div>
          )}
          
          <div className="flex justify-between">
            <span className="text-gray-600">Platform:</span>
            <span className="capitalize bg-gray-100 px-2 py-1 rounded text-sm">
              {product.platform}
            </span>
          </div>
          
          <div className="flex justify-between">
            <span className="text-gray-600">Status:</span>
            <span className={`px-2 py-1 rounded text-sm ${
              product.is_active 
                ? 'bg-green-100 text-green-800' 
                : 'bg-red-100 text-red-800'
            }`}>
              {product.is_active ? 'Active' : 'Inactive'}
            </span>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-2 mb-3">
          <button
            onClick={checkPriceNow}
            disabled={isUpdating}
            className="bg-blue-600 text-white py-2 px-3 rounded text-sm hover:bg-blue-700 disabled:opacity-50"
          >
            {isUpdating ? 'Updating...' : 'Check Price'}
          </button>
          
          <button
            onClick={fetchPriceHistory}
            className="bg-gray-600 text-white py-2 px-3 rounded text-sm hover:bg-gray-700"
          >
            Price History
          </button>
        </div>

        <div className="flex justify-between">
          <a
            href={product.url}
            target="_blank"
            rel="noopener noreferrer"
            className="bg-green-600 text-white py-2 px-3 rounded text-sm hover:bg-green-700"
          >
            View Product
          </a>
          
          <button
            onClick={deleteProduct}
            className="bg-red-600 text-white py-2 px-3 rounded text-sm hover:bg-red-700"
          >
            Delete
          </button>
        </div>

        {showPriceHistory && (
          <div className="mt-4 border-t pt-4">
            <h4 className="font-semibold mb-2">Price History</h4>
            <div className="max-h-40 overflow-y-auto">
              {priceHistory.length > 0 ? (
                priceHistory.map((entry, index) => (
                  <div key={index} className="flex justify-between text-sm py-1">
                    <span>${entry.price.toFixed(2)}</span>
                    <span className="text-gray-500">
                      {formatDate(entry.timestamp)}
                    </span>
                  </div>
                ))
              ) : (
                <p className="text-gray-500 text-sm">No price history available</p>
              )}
            </div>
            <button
              onClick={() => setShowPriceHistory(false)}
              className="mt-2 text-blue-600 text-sm hover:underline"
            >
              Hide History
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default ProductCard;
