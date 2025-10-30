import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { Document } from 'mongoose';

export type LocationDocument = Location & Document;

@Schema()
export class Location extends Document {
  @Prop({ required: true })
  placeID: string;

  @Prop({ required: true })
  name: string;

  @Prop({ required: true })
  address : string;

  @Prop({ required: true })
  longtitude: number;

  @Prop({ required: true })
  latitude: number;

  @Prop({ required: true })
  keyword: string;

  @Prop({ required: true })
  types: string;

  @Prop()
  phone: string;

  @Prop()
  website: string;

  @Prop()
  photo_1_URL: string;

  @Prop()
  review_summary: string;

  @Prop()
  user_ratings_total: number;

  @Prop()
  num_reviews: number;
  
  @Prop()
  rating: number;  
}

export const LocationSchema = SchemaFactory.createForClass(Location);
