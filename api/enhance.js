// Vercel Serverless Function for X-Ray Enhancement
const { createCanvas } = require('canvas');
const sharp = require('sharp');

export default async function handler(req, res) {
  // Enable CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { image } = req.body;

    if (!image) {
      return res.status(400).json({ error: 'No image data provided' });
    }

    // Process image (simplified version for deployment)
    const enhanced_v1 = await processImage(image, 'ai');
    const enhanced_v2 = await processImage(image, 'traditional');

    return res.status(200).json({
      enhanced_v1: enhanced_v1,
      enhanced_v2: enhanced_v2,
      message: 'X-ray images enhanced successfully'
    });

  } catch (error) {
    console.error('Enhancement error:', error);
    return res.status(500).json({ error: 'Failed to enhance image' });
  }
}

async function processImage(base64Image, type) {
  try {
    // Remove data URL prefix
    const base64Data = base64Image.replace(/^data:image\/\w+;base64,/, '');
    const buffer = Buffer.from(base64Data, 'base64');

    // Use Sharp for image processing (works in serverless)
    let processedImage;

    if (type === 'ai') {
      // Simulated AI enhancement
      processedImage = await sharp(buffer)
        .resize(512, 512, { fit: 'inside' })
        .sharpen({ sigma: 1, flat: 1, jagged: 2 })
        .normalize()
        .modulate({ brightness: 1.1, saturation: 1.2 })
        .jpeg({ quality: 90 })
        .toBuffer();
    } else {
      // Traditional enhancement
      processedImage = await sharp(buffer)
        .resize(512, 512, { fit: 'inside' })
        .contrast(1.2)
        .gamma(1.1)
        .median(3)
        .jpeg({ quality: 90 })
        .toBuffer();
    }

    // Convert back to base64
    return `data:image/jpeg;base64,${processedImage.toString('base64')}`;
    
  } catch (error) {
    console.error('Image processing error:', error);
    throw error;
  }
}
