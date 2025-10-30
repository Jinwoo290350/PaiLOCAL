import { IsString, IsNotEmpty, IsOptional, IsNumber, IsUrl } from 'class-validator';

export class CreateLocationDto {
  @IsString()
  @IsNotEmpty()
  placeID: string;

  @IsString()
  @IsNotEmpty()
  name: string;

  @IsString()
  @IsNotEmpty()
  address: string;

  @IsNumber()
  @IsNotEmpty()
  latitude: number;

  @IsNumber()
  @IsNotEmpty()
  longtitude: number;

  @IsString()
  @IsNotEmpty()
  keyword: string;

  @IsString()
  @IsNotEmpty()
  types: string;

  @IsOptional()
  @IsString()
  phone?: string;

  @IsOptional()
  @IsUrl()
  website?: string;

  @IsOptional()
  @IsString()
  photo_1_URL?: string;

  @IsOptional()
  @IsString()
  review_summary?: string;

  @IsOptional()
  @IsNumber()
  user_ratings_total?: number;

  @IsOptional()
  @IsNumber()
  num_reviews?: number;

  @IsOptional()
  @IsNumber()
  rating?: number;
}
