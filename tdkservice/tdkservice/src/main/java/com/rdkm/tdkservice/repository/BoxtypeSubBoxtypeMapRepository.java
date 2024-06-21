package com.rdkm.tdkservice.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.rdkm.tdkservice.model.BoxtypeSubBoxtypeMap;

/**
 * The BoxtypeSubBoxtypeMapRepository interface provides methods for box type
 */
@Repository
public interface BoxtypeSubBoxtypeMapRepository extends JpaRepository<BoxtypeSubBoxtypeMap, Integer> {

	/**
	 * This method is used to find a box type by name.
	 *
	 * @param boxTypeName the name of the box type to find
	 * @return a BoxType object containing the box type's information
	 */
	List<BoxtypeSubBoxtypeMap> findByBoxTypeName(String boxTypeName);

	


}
