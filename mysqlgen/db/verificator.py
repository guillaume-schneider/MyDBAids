import mysqlgen.db.blueprint as blueprint
import mysqlgen.db.abstract.abstract_type as abstract


class BlueprintVerificator:
    @staticmethod
    def verify(blueprint: blueprint.TableBlueprint):
        attr_to_remove = []
        for (name ,type_attr) in blueprint.attributes.items():
            if type_attr == abstract.AbstractType.AUTO_ID.name.lower():
                attr_to_remove.append(name)
        for name in attr_to_remove:
            blueprint.remove_attribute(name)
